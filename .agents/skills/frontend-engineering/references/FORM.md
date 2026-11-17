<!-- Source: FRONTEND_GUIDELINES(2).md, section FORM. Original rule numbers preserved, qualified with FE. -->

## FORM

- **FE.FORM1 M** Use correct input types, `name`, labels, grouping, autocomplete and validation constraints for the data and task; protect sensitive fields from unnecessary browser or telemetry exposure.
- **FE.FORM2 M** Distinguish client validation for usability from authoritative server validation for security and invariants; never trust a disabled/hidden field or frontend schema as authorization.
- **FE.FORM3 M** Keep validation error messages field-specific, understandable, programmatically associated and available after submission; preserve entered data when reasonable.
- **FE.FORM4 S** Validate at a helpful moment; avoid aggressive keystroke-level errors for incomplete values unless interaction demands them. Summarize errors for lengthy forms as appropriate.
- **FE.FORM5 M** Handle duplicate submissions, pending/disabling UI and uncertain network outcomes without assuming a request failed merely because the browser timed out.
- **FE.FORM6 S** Match required/optional wording and formats to locale; provide examples or constraints for unusual values, but do not replace labels with placeholder examples.
- **FE.FORM7 M** Do not place credentials, private content or payment secrets into URLs, analytics events, console logs or persistent browser state inadvertently.
- **FE.FORM8 S** Prefer native `FormData`/form submission and accessible input controls over bespoke state machinery where product/framework requirements permit.
- **FE.FORM9 M** Ensure validation, success and failure states can be reached and understood by keyboard and assistive technology; restore the user's editing context when feasible.
- **FE.FORM10 S** Distinguish saving a draft, committing a mutation and navigating away. Warn about unsaved changes only where data loss is real and avoid over-triggered prompts.
