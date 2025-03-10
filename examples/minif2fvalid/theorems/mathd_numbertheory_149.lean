--@funsearch.evolve
theorem mathd_numbertheory_149 :
  (∑ k in Finset.filter (fun x => x % 8 = 5 ∧ x % 6 = 3) (Finset.range 50), k) = 66 := by
  apply Eq.refl

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
