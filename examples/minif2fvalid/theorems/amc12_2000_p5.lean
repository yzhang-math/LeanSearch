--@funsearch.evolve
theorem amc12_2000_p5 (x p : ℝ) (h₀ : x < 2) (h₁ : abs (x - 2) = p) : x - p = 2 - 2 * p := by
  suffices abs (x - 2) = -(x - 2) by
    rw [h₁] at this
    linarith
  apply abs_of_neg
  linarith

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
