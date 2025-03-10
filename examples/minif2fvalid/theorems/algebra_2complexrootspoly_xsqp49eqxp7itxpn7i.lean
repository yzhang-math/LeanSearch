--@funsearch.evolve
theorem algebra_2complexrootspoly_xsqp49eqxp7itxpn7i (x : ℂ) :
    x ^ 2 + 49 = (x + 7 * Complex.I) * (x + -7 * Complex.I) := by
  simp_all only [Complex.cpow_two, neg_mul]
  ring
  simp_all only [Complex.I_sq, neg_mul, one_mul, sub_neg_eq_add]
  ring

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
