--@funsearch.evolve
theorem amc12a_2017_p2 (x y : ℝ) (h₀ : x ≠ 0) (h₁ : y ≠ 0) (h₂ : x + y = 4 * (x * y)) :
  1 / x + 1 / y = 4 := by
  simp_all only [ne_eq, one_div]
  field_simp
  rwa [add_comm]

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
