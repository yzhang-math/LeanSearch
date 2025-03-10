--@funsearch.evolve
theorem hello_world (a b c : Nat)
  : a + b + c = a + c + b := by
  rw [add_assoc, add_comm b, ←add_assoc]

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
