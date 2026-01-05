from .models import Persona
from .repository import ArbolGenealogico


class DemoDataLoader:
    """
    Clase responsable exclusivamente de cargar los datos de demostración
    de la Casa del Dragón.
    """

    @staticmethod
    def cargar_datos(arbol: ArbolGenealogico) -> None:
        """
        Carga datos de demostración del árbol genealógico de La Casa del Dragón.

        Este método orquesta la carga completa dividida por generaciones y ramas familiares.
        """
        DemoDataLoader._cargar_generacion_aegon_i(arbol)
        DemoDataLoader._cargar_hijos_aenys_i(arbol)
        DemoDataLoader._cargar_hijos_aegon_y_rhaena(arbol)
        DemoDataLoader._cargar_generacion_jaehaerys_i(arbol)
        DemoDataLoader._cargar_hijos_baelon_y_alyssa(arbol)
        DemoDataLoader._cargar_generacion_viserys_i(arbol)
        DemoDataLoader._cargar_hijos_aegon_ii(arbol)
        DemoDataLoader._cargar_generacion_daemon(arbol)
        DemoDataLoader._cargar_hijos_daemon_y_rhaenyra(arbol)
        DemoDataLoader._cargar_generacion_aegon_iii(arbol)
        DemoDataLoader._cargar_generacion_viserys_ii(arbol)

    @staticmethod
    def _remover_pareja_seguro(
        arbol: ArbolGenealogico, persona1: Persona, persona2: Persona
    ) -> None:
        """Helper para remover parejas de forma segura."""
        try:
            if persona1.pareja and persona1.pareja.id == persona2.id:
                arbol.remove_pareja(persona1, persona2)
        except ValueError:
            pass

    @staticmethod
    def _get_persona(arbol: ArbolGenealogico, nombre: str) -> Persona:
        """Recupera una persona por nombre del árbol existente."""
        for p in arbol.personas.values():
            if p.nombre == nombre:
                return p
        raise ValueError(f"Error interno: Persona '{nombre}' no encontrada durante la carga.")

    @staticmethod
    def _cargar_generacion_aegon_i(arbol: ArbolGenealogico) -> None:
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

    @staticmethod
    def _cargar_hijos_aenys_i(arbol: ArbolGenealogico) -> None:
        aenys_i = DemoDataLoader._get_persona(arbol, "Aenys I")

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

    @staticmethod
    def _cargar_hijos_aegon_y_rhaena(arbol: ArbolGenealogico) -> None:
        aegon_principe = DemoDataLoader._get_persona(arbol, "Aegon (hijo de Aenys I)")
        rhaena = DemoDataLoader._get_persona(arbol, "Rhaena")
        maegor_i = DemoDataLoader._get_persona(arbol, "Maegor I el Cruel")

        # Relaciones de Aegon y Rhaena
        arbol.add_pareja(aegon_principe, rhaena)

        # Hijas de Aegon y Rhaena
        aerea = arbol.registrar_persona("Aerea")
        rhaella = arbol.registrar_persona("Rhaella")

        for hija in [aerea, rhaella]:
            arbol.add_hijo(aegon_principe, hija)
            arbol.add_hijo(rhaena, hija)

        # Rhaena se casa con Maegor después
        DemoDataLoader._remover_pareja_seguro(arbol, aegon_principe, rhaena)
        arbol.add_pareja(maegor_i, rhaena)

    @staticmethod
    def _cargar_generacion_jaehaerys_i(arbol: ArbolGenealogico) -> None:
        jaehaerys_i = DemoDataLoader._get_persona(arbol, "Jaehaerys I el Conciliador")
        alysanne = DemoDataLoader._get_persona(arbol, "Alysanne la Bondadosa")

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
        aemon = DemoDataLoader._get_persona(arbol, "Aemon (hijo de Jaehaerys I)")
        jocelyn_baratheon = arbol.registrar_persona("Jocelyn Baratheon")
        arbol.add_pareja(aemon, jocelyn_baratheon)

        # Rhaenys (La Reina que Nunca Fue)
        rhaenys_reina = arbol.registrar_persona("Rhaenys (La Reina que Nunca Fue)")
        arbol.add_hijo(aemon, rhaenys_reina)
        arbol.add_hijo(jocelyn_baratheon, rhaenys_reina)

    @staticmethod
    def _cargar_hijos_baelon_y_alyssa(arbol: ArbolGenealogico) -> None:
        baelon = DemoDataLoader._get_persona(arbol, "Baelon")
        alyssa_targaryen = DemoDataLoader._get_persona(arbol, "Alyssa Targaryen")

        # Baelon y Alyssa (hermanos casados)
        arbol.add_pareja(baelon, alyssa_targaryen)

        # Hijos de Baelon y Alyssa
        hijos_nombres = ["Viserys I", "Daemon", "Aegon (hijo de Baelon)"]
        for nombre in hijos_nombres:
            hijo = arbol.registrar_persona(nombre)
            arbol.add_hijo(baelon, hijo)
            arbol.add_hijo(alyssa_targaryen, hijo)

    @staticmethod
    def _cargar_generacion_viserys_i(arbol: ArbolGenealogico) -> None:
        viserys_i = DemoDataLoader._get_persona(arbol, "Viserys I")

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
        DemoDataLoader._remover_pareja_seguro(arbol, viserys_i, aemma_arryn)
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

    @staticmethod
    def _cargar_hijos_aegon_ii(arbol: ArbolGenealogico) -> None:
        aegon_ii = DemoDataLoader._get_persona(arbol, "Aegon II el Usurpador")
        helaena = DemoDataLoader._get_persona(arbol, "Helaena")

        # Aegon II y Helaena (hermanos casados)
        arbol.add_pareja(aegon_ii, helaena)

        # Hijos de Aegon II y Helaena
        hijos = ["Jaehaera", "Jaehaerys (hijo de Aegon II)", "Maelor"]
        for nombre in hijos:
            hijo = arbol.registrar_persona(nombre)
            arbol.add_hijo(aegon_ii, hijo)
            arbol.add_hijo(helaena, hijo)

    @staticmethod
    def _cargar_generacion_daemon(arbol: ArbolGenealogico) -> None:
        daemon = DemoDataLoader._get_persona(arbol, "Daemon")

        # Daemon y Laena Velaryon
        laena_velaryon = arbol.registrar_persona("Laena Velaryon")
        arbol.add_pareja(daemon, laena_velaryon)

        # Hijas de Daemon y Laena Velaryon
        hijas = ["Baela", "Rhaena (hija de Daemon)"]
        for nombre in hijas:
            hija = arbol.registrar_persona(nombre)
            arbol.add_hijo(daemon, hija)
            arbol.add_hijo(laena_velaryon, hija)

    @staticmethod
    def _cargar_hijos_daemon_y_rhaenyra(arbol: ArbolGenealogico) -> None:
        daemon = DemoDataLoader._get_persona(arbol, "Daemon")
        rhaenyra = DemoDataLoader._get_persona(arbol, "Rhaenyra")
        # Recuperar pareja anterior de Daemon para removerla
        laena_velaryon = DemoDataLoader._get_persona(arbol, "Laena Velaryon")

        # Daemon se casa con Rhaenyra (sobrina)
        DemoDataLoader._remover_pareja_seguro(arbol, daemon, laena_velaryon)
        arbol.add_pareja(daemon, rhaenyra)

        # Hijos de Daemon y Rhaenyra
        hijos = ["Aegon III Veneno de Dragón", "Viserys II", "Visenya (hija de Rhaenyra)"]
        for nombre in hijos:
            hijo = arbol.registrar_persona(nombre)
            arbol.add_hijo(daemon, hijo)
            arbol.add_hijo(rhaenyra, hijo)

    @staticmethod
    def _cargar_generacion_aegon_iii(arbol: ArbolGenealogico) -> None:
        aegon_iii = DemoDataLoader._get_persona(arbol, "Aegon III Veneno de Dragón")
        aegon_ii = DemoDataLoader._get_persona(arbol, "Aegon II el Usurpador")
        jaehaera = DemoDataLoader._get_persona(arbol, "Jaehaera")

        # Jaehaera se casa con Aegon III (después de la muerte de Aegon II)
        # Nota: Aegon II ya no es pareja de Jaehaera (eran padre e hija, no pareja,
        # pero el código original removía pareja entre ellos, quizás por error de copy-paste
        # o interpretando una regla de "custodia". El código original asumía pareja.)
        # CORRECCIÓN SOBRE ORIGINAL: El código original hacía:
        # _remover_pareja_seguro(arbol, aegon_ii, jaehaera)
        # Pero Aegon II es PADRE de Jaehaera, no pareja.
        # Mantendremos la lógica original por compatibilidad aunque sea extraña,
        # o asumimos que se refería a limpiar estado.
        DemoDataLoader._remover_pareja_seguro(arbol, aegon_ii, jaehaera)
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
        baelor_i = DemoDataLoader._get_persona(arbol, "Baelor I el Bendito")
        daena = DemoDataLoader._get_persona(arbol, "Daena la Rebelde")
        arbol.add_pareja(baelor_i, daena)

    @staticmethod
    def _cargar_generacion_viserys_ii(arbol: ArbolGenealogico) -> None:
        viserys_ii = DemoDataLoader._get_persona(arbol, "Viserys II")

        # Viserys II se casa con Larra Rogare
        larra_rogare = arbol.registrar_persona("Larra Rogare")
        arbol.add_pareja(viserys_ii, larra_rogare)

        # Hijos de Viserys II y Larra Rogare
        hijos = ["Aegon IV el Indigno", "Aemon el Caballero Dragón", "Naerys"]
        for nombre in hijos:
            hijo = arbol.registrar_persona(nombre)
            arbol.add_hijo(viserys_ii, hijo)
            arbol.add_hijo(larra_rogare, hijo)

        aegon_iv = DemoDataLoader._get_persona(arbol, "Aegon IV el Indigno")
        naerys = DemoDataLoader._get_persona(arbol, "Naerys")

        # Aegon IV y Naerys (hermanos casados)
        arbol.add_pareja(aegon_iv, naerys)

        # Daeron II
        daeron_ii = arbol.registrar_persona("Daeron II")
        arbol.add_hijo(aegon_iv, daeron_ii)
        arbol.add_hijo(naerys, daeron_ii)

        # Daemon Fuegoscuro (hijo de Aegon IV y Daena la Rebelde)
        daena = DemoDataLoader._get_persona(arbol, "Daena la Rebelde")
        daemon_fuegoscuro = arbol.registrar_persona("Daemon Fuegoscuro")
        arbol.add_hijo(aegon_iv, daemon_fuegoscuro)
        arbol.add_hijo(daena, daemon_fuegoscuro)
