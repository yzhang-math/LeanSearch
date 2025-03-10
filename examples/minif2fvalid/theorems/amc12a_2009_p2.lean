--@funsearch.evolve
theorem amc12a_2009_p2 : 1 + 1 / (1 + 1 / (1 + 1)) = (5 : ℚ) / 3 := by
  simp_all only [one_div]
  norm_num

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
