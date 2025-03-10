--@funsearch.evolve
theorem amc12b_2003_p9 (a b : ℝ) (f : ℝ → ℝ) (h₀ : ∀ x, f x = a * x + b) (h₁ : f 6 - f 2 = 12) :
    f 12 - f 2 = 30 := by
  simp_all only [add_sub_add_right_eq_sub]
  linarith

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
