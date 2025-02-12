--@funsearch.evolve
theorem pi_eq_sum_univ {ι : Type*} [Fintype ι] [DecidableEq ι] {R : Type*} [Semiring R] (x : ι → R) : x = ∑ i, (x i) • fun j => if i = j then (1 : R) else 0 := by
  sorry
  -- the theorem you want to prove

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
  sorry
  -- this theorem is irrelevant, but needs to be there with the .run header, until I figure out how to do this better
