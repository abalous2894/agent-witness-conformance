# Claim boundary

AWC v0.1 grades **consistency between a reference trace and an evidence bundle** under explicit completeness claims. It does **not** by itself establish:

- That the reference trace matches physical production execution.  
- Cryptographic non-repudiation, timestamps in Rekor, or third-party witness cosign (future profiles).  
- Behavioral policy compliance (refunds, prohibited tools) — see WitnessDiff behavioral lane.  
- Model identity, checkpoint binding, or sovereign inference attestation.

**If the reference is wrong or incomplete, AWC cannot fix that.** It tests whether the export **supports the completeness story it tells** relative to the reference you supplied.
