--@funsearch.evolve
theorem pi_eq_sum_univ {ι : Type*} [Fintype ι] [DecidableEq ι] {R : Type*} [Semiring R] (x : ι → R) : x = ∑ i, (x i) • fun j => if i = j then (1 : R) else 0 := by
  sorry
  -- the theorem you want to prove

--@funsearch.run
theorem irrelevant : 2 + 3 = 3 + 2 := by
  sorry
  -- this theorem is irrelevant, but needs to be there with the .run header, until I figure out how to do this better


theorem amc12a_2015_p10_v1 (x y : ℤ) (h₀ : 0 < y) (h₁ : y < x) (h₂ : x + y + x * y = 80) : x = 26 := by
  have key : x + y + x * y = 80
  rw [← h₂]
  have : x * y + x + y = 80
  rw [add_comm]
  have : x * (y + 1) + y = 80
  have : x * (y + 1) = 80 - y
  have h_range : 1 ≤ y ∧ y < x
  exact ⟨by linarith, h₁⟩
  have : x = (80 - y) / (y + 1)
  have : y = 6 ∧ x = 26
  apply Eq.symm
