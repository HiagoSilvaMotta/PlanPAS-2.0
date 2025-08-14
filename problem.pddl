(define (problem more)
(:domain sorting)
    
    (:objects
        atuador_simples1 atuador_simples2 atuador_duplo1 - atuador
        box1 box2 box3 - destino

        esteira - esteira
        inicio - inicio
        peqnmet1 peqmet1 mednmet1 medmet1 grdnmet1 grdmet1 - caracteristica

        item0 - objeto
        item1 - objeto
        item2 - objeto
        item3 - objeto
        item4 - objeto
        item5 - objeto
        item6 - objeto
        item7 - objeto
        	
    )
    
    (:init
	(link atuador_simples1 box1)
        (link atuador_simples2 box2)
        (link atuador_duplo1 box3)

        (type item0 peqmet1)
        (type item1 peqmet1)
        (type item2 medmet1)
        (type item3 medmet1)
        (type item4 medmet1)
        (type item5 medmet1)
        (type item6 grdmet1)
        (type item7 grdmet1)
        
        (at item0 inicio)
        (at item1 inicio)
        (at item2 inicio)
        (at item3 inicio)
        (at item4 inicio)
        (at item5 inicio)
        (at item6 inicio)
        (at item7 inicio)
        	
        (not (ligado esteira))
    )
    
    (:goal (and
        (at item0 box1)
        (at item1 box3)
        (at item2 box1)
        (at item3 box1)
        (at item4 box2)
        (at item5 box2)
        (at item6 box3)
        (at item7 box3)
        		
        (not (ligado esteira))
        (not (extended atuador_simples1))
        (not (extended atuador_simples2))
        (not (extended atuador_duplo1))
        )
    )
)