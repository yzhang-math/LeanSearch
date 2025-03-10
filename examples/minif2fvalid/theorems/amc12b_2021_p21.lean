--@funsearch.evolve
theorem amc12b_2021_p21 (S : Finset ℝ)
  (h₀ : ∀ x : ℝ, x ∈ S ↔ 0 < x ∧ x ^ (2 : ℝ) ^ Real.sqrt 2 = Real.sqrt 2 ^ (2 : ℝ) ^ x) :
  (↑2 ≤ ∑ k in S, k) ∧ (∑ k in S, k) < 6 := by
  sorry

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
