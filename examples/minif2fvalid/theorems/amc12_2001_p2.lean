--@funsearch.evolve
theorem amc12_2001_p2 (a b n : ℕ) (h₀ : 1 ≤ a ∧ a ≤ 9) (h₁ : 0 ≤ b ∧ b ≤ 9) (h₂ : n = 10 * a + b)
  (h₃ : n = a * b + a + b) : b = 9 := by
  rw [h₂] at h₃
  simp at h₃
  have h₄ : 10 * a = (b + 1) * a := by linarith
  simp at h₄
  cases' h₄ with h₅ h₆
  linarith
  exfalso
  simp_all [le_refl]

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
   sorry
