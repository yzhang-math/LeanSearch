--@funsearch.evolve
theorem mathd_numbertheory_211 :
  Finset.card (Finset.filter (fun n => 6 ∣ 4 * ↑n - (2 : ℤ)) (Finset.range 60)) = 20 := by
  apply Eq.refl

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
