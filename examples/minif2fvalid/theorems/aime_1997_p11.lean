--@funsearch.evolve
theorem aime_1997_p11 (x : ℝ)
    (h₀ :
      x =
        (∑ n in Finset.Icc (1 : ℕ) 44, Real.cos (n * π / 180)) /
          ∑ n in Finset.Icc (1 : ℕ) 44, Real.sin (n * π / 180)) :
    Int.floor (100 * x) = 241 := by
  sorry

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
