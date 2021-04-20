;; Move a car from place1 to place2
(define (problem transport)
    (:domain transport)
    (:objects car1 place1 place2 box1 box2)
    (:init
        (car car1)
        (place place1)
        (place place2)
        (box box1)
        (box box2)
        (empty car1)
        (at car1 place1)
    )
    (:goal (and
        (at car1 place2)
    ))
)
