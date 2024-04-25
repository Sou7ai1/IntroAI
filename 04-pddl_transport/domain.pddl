(define (domain transport)
  (:requirements :strips)
  (:predicates
    (at ?obj - box ?loc - place)
    (at ?obj - car ?loc - place)
    (connected ?loc1 - place ?loc2 - place)
  )

  (:action load
    :parameters (?b - box ?c - car ?p - place)
    :precondition (and (at ?b ?p) (at ?c ?p) (empty ?c))
    :effect (and (in ?b ?c) (not (at ?b ?p)) (not (empty ?c)))
  )

  (:action unload
    :parameters (?b - box ?c - car ?p - place)
    :precondition (and (in ?b ?c) (at ?c ?p))
    :effect (and (at ?b ?p) (empty ?c) (not (in ?b ?c)))
  )

  (:action move
    :parameters (?c - car ?from - place ?to - place)
    :precondition (and (at ?c ?from) (empty ?c) (connected ?from ?to))
    :effect (and (at ?c ?to) (not (at ?c ?from)))
  )
)
