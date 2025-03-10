--@funsearch.evolve
theorem mathd_algebra_67 (f g : ℝ → ℝ) (h₀ : ∀ x, f x = 5 * x + 3) (h₁ : ∀ x, g x = x ^ 2 - 2) :
    g (f (-1)) = 2 := by
  simp_all only [rpow_two, mul_neg, mul_one]
  norm_num

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
