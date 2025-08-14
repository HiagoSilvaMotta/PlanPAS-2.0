(define (problem more)
(:domain sorting)
    
    (:objects
        atuador_simples1 atuador_simples2 atuador_duplo1 - atuador
        box1 box2 box3 - destino

        esteira - esteira
        inicio - inicio
        peqnmet1 peqmet1 mednmet1 medmet1 grdnmet1 grdmet1 - caracteristica

	##definir_itens
	
    )
    
    (:init
	(link atuador_simples1 box1)
        (link atuador_simples2 box2)
        (link atuador_duplo1 box3)

	##definir_tipos

	##definir_inicio
	
        (not (ligado esteira))
    )
    
    (:goal (and
        ##definir_destino
		
        (not (ligado esteira))
        (not (extended atuador_simples1))
        (not (extended atuador_simples2))
        (not (extended atuador_duplo1))
        )
    )
)