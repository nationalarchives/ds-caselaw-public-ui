function getCourtCheckboxes(root: ParentNode): HTMLInputElement[] {
  return [...root.querySelectorAll<HTMLInputElement>('input[name="court"]')];
}

function setCourtsChecked(courts: HTMLInputElement[], checked: boolean): void {
  courts.forEach((court) => {
    court.checked = checked;
  });
}

function updateGroupSelection(group: Element): void {
  const control = group.querySelector<HTMLInputElement>("[data-group-toggle]");
  if (!control) return;

  const children = getCourtCheckboxes(group);
  const selected = children.filter((court) => court.checked).length;
  control.hidden = false;
  control.checked = selected === children.length;
  control.indeterminate = selected > 0 && selected < children.length;
}

function updateScopeSelection(
  toggle: HTMLInputElement,
  label: Element,
  courts: HTMLInputElement[],
  groups: Element[],
): void {
  const count = courts.filter((court) => court.checked).length;
  toggle.checked = courts.length > 0 && count === courts.length;
  toggle.indeterminate = count > 0 && count < courts.length;
  label.textContent = toggle.checked ? "Deselect all" : "Select all";
  groups.forEach(updateGroupSelection);
}

function setupScopeToggle(
  toggle: HTMLInputElement,
  courts: HTMLInputElement[],
  update: () => void,
): void {
  if (toggle.checked) setCourtsChecked(courts, true);

  toggle.addEventListener("change", () => {
    setCourtsChecked(courts, toggle.checked);
    update();
  });
}

function setupGroupToggle(group: Element, update: () => void): void {
  const control = group.querySelector<HTMLInputElement>("[data-group-toggle]");
  control?.addEventListener("change", () => {
    setCourtsChecked(getCourtCheckboxes(group), control.checked);
    update();
  });
}

function setupCourtScopeSection(section: Element): void {
  const toggle = section.querySelector<HTMLInputElement>("[data-scope-toggle]");
  const label = section.querySelector("[data-scope-label]");
  if (!toggle || !label) return;

  const courts = getCourtCheckboxes(section);
  const groups = [...section.querySelectorAll("[data-court-group]")];
  const update = () => updateScopeSelection(toggle, label, courts, groups);

  setupScopeToggle(toggle, courts, update);
  groups.forEach((group) => setupGroupToggle(group, update));
  courts.forEach((court) => court.addEventListener("change", update));
  update();
}

export function setupCourtScopeFilters(root: ParentNode = document): void {
  root.querySelectorAll("[data-court-scope]").forEach(setupCourtScopeSection);
  const forms = new Set(
    [...root.querySelectorAll<HTMLInputElement>("[data-scope-toggle]")].map(
      (toggle) => toggle.form,
    ),
  );
  forms.forEach((form) =>
    form?.addEventListener("formdata", (event) => {
      const scopes = event.formData.getAll("scope");
      const hasCourtsOutsideScope = [
        ...form.querySelectorAll("[data-court-scope]"),
      ].some(
        (section) =>
          !scopes.includes(
            section.querySelector<HTMLInputElement>("[data-scope-toggle]")
              ?.value ?? "",
          ) && section.querySelector('input[name="court"]:checked'),
      );

      if (!scopes.includes("all_courts") && hasCourtsOutsideScope) {
        event.formData.delete("scope");
        return;
      }

      if (
        scopes.includes("all_courts") ||
        (scopes.includes("higher_courts") && scopes.includes("other_courts"))
      ) {
        event.formData.set("scope", "all_courts");
      }
      if (form.querySelector("[data-scope-toggle]:checked"))
        event.formData.delete("court");
    }),
  );
}
