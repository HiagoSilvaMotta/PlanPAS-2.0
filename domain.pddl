(define (domain sorting)
    (:requirements :typing)

    (:types
        ;; tipos de objetos
        atuador
        objeto
        inicio destino - local
        esteira
        caracteristica
    )

    (:predicates
        ;;Estado do atuador
        (extended ?atuador - atuador)
        
        ;;Estado da esteira
        (ligado ?e - esteira)
        
        ;;Local do objeto
        (at ?o - objeto ?l - local)
        
        ;;Sensor de final de curso
        (s_fimdecurso ?a - atuador)
        
        ;;Tipo do objeto
        (type ?o - objeto ?c - caracteristica)
        
        (blocked ?e - esteira)
        
        (link ?a - atuador ?d - destino)
        
    )

    ;; ligar a esteira
    (:action ligar_esteira
        :parameters (?e - esteira)
        :precondition (and
            (not (ligado ?e))
        )
        :effect (and
            (ligado ?e)
        )
    )

    ;; desligar a esteira
    (:action desligar_esteira
        :parameters (?e - esteira)
        :precondition (and
            (not(blocked ?e))
            (ligado ?e)
        )
        :effect (and
            (not (ligado ?e))
        )
    )
    
    ;; Extende o atuador
    (:action extende_atuador
        :parameters(?e - esteira ?a - atuador ?i - inicio ?d - destino ?o - objeto ?c - caracteristica)
        :precondition (and
            (type ?o ?c)
            (ligado ?e)
            (not (extended ?a))
            (at ?o ?i)
            (not(blocked ?e))
            (link ?a ?d)
        )
        :effect (and
            (at ?o ?d)
            (not (at ?o ?i))
            (extended ?a)
            (s_fimdecurso ?a)
            (blocked ?e)
        )
    )
    
    ;; Retrai o atuador
    (:action retrai_atuador
        :parameters(?e - esteira ?a - atuador )
        :precondition (and
            (s_fimdecurso ?a)
            (extended ?a)
            (blocked ?e)
        )
        :effect (and
            (not (extended ?a))
            (not (s_fimdecurso ?a))
            (not(blocked ?e))
        )
    )
)
 