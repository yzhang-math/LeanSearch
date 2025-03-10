--@funsearch.evolve
theorem mathd_algebra_31 (x : NNReal) (u : ℕ → NNReal) (h₀ : ∀ n, u (n + 1) = NNReal.sqrt (x + u n))
  (h₁ : Filter.Tendsto u Filter.atTop (𝓝 9)) : 9 = NNReal.sqrt (x + 9) := by
  sorry

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
