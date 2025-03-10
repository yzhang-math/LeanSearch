--@funsearch.evolve
theorem mathd_algebra_251 (x : ℝ) (h₀ : x ≠ 0) (h₁ : 3 + 1 / x = 7 / x) : x = 2 := by
  simp_all only [ne_eq, one_div]
  field_simp [h₀] at h₁
  linarith

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
