;; A car is needed for transportation
(define (problem transport)
    (:domain transport)
    (:objects car1 place1 place2 box1 box2)
    (:init
        (place place1)
        (place place2)
        (box box1)
        (box box2)
        (at box1 place1)
    )
    (:goal (and
        (at box1 place2)
    ))
)
