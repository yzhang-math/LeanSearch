--@funsearch.evolve
theorem foo (a : Nat) : a + 1 = Nat.succ a := by
   rfl

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
