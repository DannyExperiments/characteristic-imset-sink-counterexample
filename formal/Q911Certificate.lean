import Std

namespace SinkImset

def skeleton : List (Nat × Nat) := [(0,1),(0,2),(0,3),(0,4),(1,2),(1,3)]
def orderD : List Nat := [4,2,0,3,1]
def orderT : List Nat := [4,0,3,1,2]
def orderU : List Nat := [4,0,3,2,1]
def orderV : List Nat := [4,2,0,1,3]

def arcs (order : List Nat) : List (Nat × Nat) :=
  skeleton.map fun (u,v) => if order.idxOf u < order.idxOf v then (u,v) else (v,u)

def sinkArcs (edges : List (Nat × Nat)) (v : Nat) : List (Nat × Nat) :=
  edges.map fun (a,b) => if a == v then (b,a) else (a,b)

def imset (order : List Nat) (s : Nat) : Nat :=
  let present := (List.range 5).filter s.testBit
  if present.length < 2 then 0
  else if present.any (fun v => present.all (fun u => u == v || (arcs order).contains (u,v)))
  then 1 else 0

def support (order : List Nat) : List Nat :=
  (List.range 32).filter fun s => imset order s == 1

theorem exact_sink : sinkArcs (arcs orderD) 2 = arcs orderT := by decide +kernel

theorem distinct_supports : ([orderD,orderT,orderU,orderV].map support).Nodup := by
  decide +kernel

theorem midpoint :
  (List.range 32).all (fun s =>
    imset orderD s + imset orderT s == imset orderU s + imset orderV s) = true := by
  decide +kernel

theorem nonconstant_coordinates :
  ((List.range 32).filter fun s => imset orderD s != imset orderT s) = [14,15,21] := by
  decide +kernel

#print axioms exact_sink
#print axioms distinct_supports
#print axioms midpoint
#print axioms nonconstant_coordinates

end SinkImset
