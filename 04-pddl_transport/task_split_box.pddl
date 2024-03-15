;; Cannot split a box
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
        (at box1 place1)
        (at car1 place2)
    )
    (:goal (and
        (at box1 place2)
        (at box1 place1)
    ))
)
