from typing import TYPE_CHECKING

from .models import Persona

if TYPE_CHECKING:
    from .interfaces import ArbolRepository

from .exceptions import (
    ArbolGenealogicoError,
    ParejaNoExisteError,
    PersonaNoEncontradaError,
)

# Para type hints usamos el Protocol, pero en runtime puede ser cualquier implementación
from .interfaces import ArbolRepository


class DataLoaderDemo:
    """
    Clase responsable exclusivamente de cargar los datos de demostración
    de la Casa del Dragón.
    """

    def cargar_datos(self, arbol: "ArbolRepository") -> None:
        """
        Carga datos de demostración del árbol genealógico de La Casa del Dragón.

        Este método orquesta la carga completa dividida por generaciones y ramas familiares.

        Args:
            arbol: Repositorio del árbol genealógico donde se cargarán los datos.
        """
        self._cargar_generacion_aegon_i(arbol)
        self._cargar_hijos_aenys_i(arbol)
        self._cargar_hijos_aegon_y_rhaena(arbol)
        self._cargar_generacion_jaehaerys_i(arbol)
        self._cargar_hijos_baelon_y_alyssa(arbol)
        self._cargar_generacion_viserys_i(arbol)
        self._cargar_hijos_aegon_ii(arbol)
        self._cargar_generacion_daemon(arbol)
        self._cargar_hijos_daemon_y_rhaenyra(arbol)
        self._cargar_generacion_aegon_iii(arbol)
        self._cargar_generacion_viserys_ii(arbol)

    def _remover_pareja_seguro(
        self, arbol: "ArbolRepository", persona1: Persona, persona2: Persona
    ) -> None:
        """Helper para remover parejas de forma segura."""
        try:
            if persona1.pareja and persona1.pareja.id == persona2.id:
                arbol.remove_pareja(persona1, persona2)
        except (ParejaNoExisteError, ArbolGenealogicoError):
            pass

    def _get_persona(self, arbol: "ArbolRepository", nombre: str) -> Persona:
        """Recupera una persona por nombre del árbol existente."""
        for p in arbol.personas.values():
            if p.nombre == nombre:
                return p
        raise PersonaNoEncontradaError(
            persona_id=None,
            message=f"Error interno: Persona '{nombre}' no encontrada durante la carga."
        )

    def _cargar_generacion_aegon_i(self, arbol: "ArbolRepository") -> None:
        # Aegon I y sus esposas
        aegon_i = arbol.registrar_persona("Aegon I")
        rhaenys = arbol.registrar_persona("Rhaenys")
        visenya = arbol.registrar_persona("Visenya")
        arbol.add_pareja(aegon_i, rhaenys)

        # Hijos de Aegon I
        aenys_i = arbol.registrar_persona("Aenys I")
        maegor_i = arbol.registrar_persona("Maegor I el Cruel")

        arbol.add_hijo(aegon_i, aenys_i)
        arbol.add_hijo(rhaenys, aenys_i)
        arbol.add_hijo(aegon_i, maegor_i)
        arbol.add_hijo(visenya, maegor_i)

    def _cargar_hijos_aenys_i(self, arbol: "ArbolRepository") -> None:
        aenys_i = self._get_persona(arbol, "Aenys I")

        # Alyssa Velaryon, esposa de Aenys I
        alyssa_velaryon = arbol.registrar_persona("Alyssa Velaryon")
        arbol.add_pareja(aenys_i, alyssa_velaryon)

        # Hijos de Aenys I
        hijos = [
            "Aegon (hijo de Aenys I)",
            "Rhaena",
            "Viserys (hijo de Aenys I)",
            "Jaehaerys I el Conciliador",
            "Alysanne la Bondadosa",
            "Vaella",
        ]

        for nombre_hijo in hijos:
            hijo = arbol.registrar_persona(nombre_hijo)
            arbol.add_hijo(aenys_i, hijo)
            arbol.add_hijo(alyssa_velaryon, hijo)

    def _cargar_hijos_aegon_y_rhaena(self, arbol: "ArbolRepository") -> None:
        aegon_principe = self._get_persona(arbol, "Aegon (hijo de Aenys I)")
        rhaena = self._get_persona(arbol, "Rhaena")
        maegor_i = self._get_persona(arbol, "Maegor I el Cruel")

        # Relaciones de Aegon y Rhaena
        arbol.add_pareja(aegon_principe, rhaena)

        # Hijas de Aegon y Rhaena
        aerea = arbol.registrar_persona("Aerea")
        rhaella = arbol.registrar_persona("Rhaella")

        for hija in [aerea, rhaella]:
            arbol.add_hijo(aegon_principe, hija)
            arbol.add_hijo(rhaena, hija)

        # Rhaena se casa con Maegor después
        self._remover_pareja_seguro(arbol, aegon_principe, rhaena)
        arbol.add_pareja(maegor_i, rhaena)

    def _cargar_generacion_jaehaerys_i(self, arbol: "ArbolRepository") -> None:
        jaehaerys_i = self._get_persona(arbol, "Jaehaerys I el Conciliador")
        alysanne = self._get_persona(arbol, "Alysanne la Bondadosa")

        # Jaehaerys I y Alysanne (hermanos casados)
        arbol.add_pareja(jaehaerys_i, alysanne)

        # Hijos de Jaehaerys I y Alysanne
        hijos_nombres = [
            "Aegon (hijo de Jaehaerys I)",
            "Daenerys (hija de Jaehaerys I)",
            "Aemon (hijo de Jaehaerys I)",
            "Baelon",
            "Alyssa Targaryen",
            "Maegelle",
            "Vaegon",
            "Daella",
            "Saera",
            "Viserra",
            "Gaemon",
            "Valerion",
            "Gael",
        ]

        for nombre in hijos_nombres:
            hijo = arbol.registrar_persona(nombre)
            arbol.add_hijo(jaehaerys_i, hijo)
            arbol.add_hijo(alysanne, hijo)

        # Aemon se casa con Jocelyn Baratheon
        aemon = self._get_persona(arbol, "Aemon (hijo de Jaehaerys I)")
        jocelyn_baratheon = arbol.registrar_persona("Jocelyn Baratheon")
        arbol.add_pareja(aemon, jocelyn_baratheon)

        # Rhaenys (La Reina que Nunca Fue)
        rhaenys_reina = arbol.registrar_persona("Rhaenys (La Reina que Nunca Fue)")
        arbol.add_hijo(aemon, rhaenys_reina)
        arbol.add_hijo(jocelyn_baratheon, rhaenys_reina)

    def _cargar_hijos_baelon_y_alyssa(self, arbol: "ArbolRepository") -> None:
        baelon = self._get_persona(arbol, "Baelon")
        alyssa_targaryen = self._get_persona(arbol, "Alyssa Targaryen")

        # Baelon y Alyssa (hermanos casados)
        arbol.add_pareja(baelon, alyssa_targaryen)

        # Hijos de Baelon y Alyssa
        hijos_nombres = ["Viserys I", "Daemon", "Aegon (hijo de Baelon)"]
        for nombre in hijos_nombres:
            hijo = arbol.registrar_persona(nombre)
            arbol.add_hijo(baelon, hijo)
            arbol.add_hijo(alyssa_targaryen, hijo)

    def _cargar_generacion_viserys_i(self, arbol: "ArbolRepository") -> None:
        viserys_i = self._get_persona(arbol, "Viserys I")

        # Viserys I - Primer matrimonio con Aemma Arryn
        aemma_arryn = arbol.registrar_persona("Aemma Arryn")
        arbol.add_pareja(viserys_i, aemma_arryn)

        # Hijos de Viserys I y Aemma Arryn
        rhaenyra = arbol.registrar_persona("Rhaenyra")
        baelon_vis = arbol.registrar_persona("Baelon (hijo de Viserys I)")

        for hijo in [rhaenyra, baelon_vis]:
            arbol.add_hijo(viserys_i, hijo)
            arbol.add_hijo(aemma_arryn, hijo)

        # Viserys I - Segundo matrimonio con Alicent Hightower
        alicent_hightower = arbol.registrar_persona("Alicent Hightower")
        self._remover_pareja_seguro(arbol, viserys_i, aemma_arryn)
        arbol.add_pareja(viserys_i, alicent_hightower)

        # Hijos de Viserys I y Alicent Hightower
        hijos_alicent = [
            "Aegon II el Usurpador",
            "Aemond el Tuerto",
            "Helaena",
            "Daeron el Atrevido",
        ]
        for nombre in hijos_alicent:
            hijo = arbol.registrar_persona(nombre)
            arbol.add_hijo(viserys_i, hijo)
            arbol.add_hijo(alicent_hightower, hijo)

    def _cargar_hijos_aegon_ii(self, arbol: "ArbolRepository") -> None:
        aegon_ii = self._get_persona(arbol, "Aegon II el Usurpador")
        helaena = self._get_persona(arbol, "Helaena")

        # Aegon II y Helaena (hermanos casados)
        arbol.add_pareja(aegon_ii, helaena)

        # Hijos de Aegon II y Helaena
        hijos = ["Jaehaera", "Jaehaerys (hijo de Aegon II)", "Maelor"]
        for nombre in hijos:
            hijo = arbol.registrar_persona(nombre)
            arbol.add_hijo(aegon_ii, hijo)
            arbol.add_hijo(helaena, hijo)

    def _cargar_generacion_daemon(self, arbol: "ArbolRepository") -> None:
        daemon = self._get_persona(arbol, "Daemon")

        # Daemon y Laena Velaryon
        laena_velaryon = arbol.registrar_persona("Laena Velaryon")
        arbol.add_pareja(daemon, laena_velaryon)

        # Hijas de Daemon y Laena Velaryon
        hijas = ["Baela", "Rhaena (hija de Daemon)"]
        for nombre in hijas:
            hija = arbol.registrar_persona(nombre)
            arbol.add_hijo(daemon, hija)
            arbol.add_hijo(laena_velaryon, hija)

    def _cargar_hijos_daemon_y_rhaenyra(self, arbol: "ArbolRepository") -> None:
        daemon = self._get_persona(arbol, "Daemon")
        rhaenyra = self._get_persona(arbol, "Rhaenyra")
        # Recuperar pareja anterior de Daemon para removerla
        laena_velaryon = self._get_persona(arbol, "Laena Velaryon")

        # Daemon se casa con Rhaenyra (sobrina)
        self._remover_pareja_seguro(arbol, daemon, laena_velaryon)
        arbol.add_pareja(daemon, rhaenyra)

        # Hijos de Daemon y Rhaenyra
        hijos = ["Aegon III Veneno de Dragón", "Viserys II", "Visenya (hija de Rhaenyra)"]
        for nombre in hijos:
            hijo = arbol.registrar_persona(nombre)
            arbol.add_hijo(daemon, hijo)
            arbol.add_hijo(rhaenyra, hijo)

    def _cargar_generacion_aegon_iii(self, arbol: "ArbolRepository") -> None:
        aegon_iii = self._get_persona(arbol, "Aegon III Veneno de Dragón")
        aegon_ii = self._get_persona(arbol, "Aegon II el Usurpador")
        jaehaera = self._get_persona(arbol, "Jaehaera")

        # Jaehaera se casa con Aegon III (después de la muerte de Aegon II)
        # Nota: Aegon II ya no es pareja de Jaehaera (eran padre e hija, no pareja,
        # pero el código original removía pareja entre ellos, quizás por error de copy-paste
        # o interpretando una regla de "custodia". El código original asumía pareja.)
        # CORRECCIÓN SOBRE ORIGINAL: El código original hacía:
        # _remover_pareja_seguro(arbol, aegon_ii, jaehaera)
        # Pero Aegon II es PADRE de Jaehaera, no pareja.
        # Mantendremos la lógica original por compatibilidad aunque sea extraña,
        # o asumimos que se refería a limpiar estado.
        self._remover_pareja_seguro(arbol, aegon_ii, jaehaera)
        arbol.add_pareja(aegon_iii, jaehaera)

        # Hijos de Aegon III (con otra esposa, no especificada en el texto)
        hijos = [
            "Daeron I el Joven Dragón",
            "Baelor I el Bendito",
            "Daena la Rebelde",
            "Elaena",
            "Rhaena (septa)",
        ]

        for nombre in hijos:
            hijo = arbol.registrar_persona(nombre)
            arbol.add_hijo(aegon_iii, hijo)

        # Baelor I y Daena (hermanos casados, no consumado)
        baelor_i = self._get_persona(arbol, "Baelor I el Bendito")
        daena = self._get_persona(arbol, "Daena la Rebelde")
        arbol.add_pareja(baelor_i, daena)

    def _cargar_generacion_viserys_ii(self, arbol: "ArbolRepository") -> None:
        viserys_ii = self._get_persona(arbol, "Viserys II")

        # Viserys II se casa con Larra Rogare
        larra_rogare = arbol.registrar_persona("Larra Rogare")
        arbol.add_pareja(viserys_ii, larra_rogare)

        # Hijos de Viserys II y Larra Rogare
        hijos = ["Aegon IV el Indigno", "Aemon el Caballero Dragón", "Naerys"]
        for nombre in hijos:
            hijo = arbol.registrar_persona(nombre)
            arbol.add_hijo(viserys_ii, hijo)
            arbol.add_hijo(larra_rogare, hijo)

        aegon_iv = self._get_persona(arbol, "Aegon IV el Indigno")
        naerys = self._get_persona(arbol, "Naerys")

        # Aegon IV y Naerys (hermanos casados)
        arbol.add_pareja(aegon_iv, naerys)

        # Daeron II
        daeron_ii = arbol.registrar_persona("Daeron II")
        arbol.add_hijo(aegon_iv, daeron_ii)
        arbol.add_hijo(naerys, daeron_ii)

        # Daemon Fuegoscuro (hijo de Aegon IV y Daena la Rebelde)
        daena = self._get_persona(arbol, "Daena la Rebelde")
        daemon_fuegoscuro = arbol.registrar_persona("Daemon Fuegoscuro")
        arbol.add_hijo(aegon_iv, daemon_fuegoscuro)
        arbol.add_hijo(daena, daemon_fuegoscuro)
