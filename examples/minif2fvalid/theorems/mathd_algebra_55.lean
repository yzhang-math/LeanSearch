--@funsearch.evolve
theorem mathd_algebra_55 (q p : ℝ) (h₀ : q = 2 - 4 + 6 - 8 + 10 - 12 + 14)
  (h₁ : p = 3 - 6 + 9 - 12 + 15 - 18 + 21) : q / p = 2 / 3 := by
  subst h₁ h₀
  norm_num

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
