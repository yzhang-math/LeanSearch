--@funsearch.evolve
theorem amc12a_2021_p7 (x y : ℝ) : 1 ≤ (x * y - 1) ^ 2 + (x + y) ^ 2 := by
  simp only [sub_eq_add_neg, add_right_comm]
  ring
  nlinarith

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
