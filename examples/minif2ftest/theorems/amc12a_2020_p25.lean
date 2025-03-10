--@funsearch.evolve
theorem amc12a_2020_p25
  (a : ℚ)
  (S : Finset ℝ)
  (h₀ : ∀ (x : ℝ), x ∈ S ↔ ↑⌊x⌋ * (x - ↑⌊x⌋) = ↑a * x ^ 2)
  (h₁ : ∑ k in S, k = 420) :
  ↑a.den + a.num = 929 := by sorry

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
