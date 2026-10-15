export function setupCourtScopeFilters(root = document) {
    root.querySelectorAll("[data-court-scope]").forEach((section) => {
        const toggle = section.querySelector("[data-scope-toggle]");
        const label = section.querySelector("[data-scope-label]");
        const courts = [...section.querySelectorAll('input[name="court"]')];
        const groups = [...section.querySelectorAll("[data-court-group]")];
        const update = () => {
            const count = courts.filter((court) => court.checked).length;
            toggle.checked = courts.length > 0 && count === courts.length;
            toggle.indeterminate = count > 0 && count < courts.length;
            label.textContent = toggle.checked ? "Deselect all" : "Select all";
            groups.forEach((group) => {
                const control = group.querySelector("[data-group-toggle]");
                if (!control) return;
                const children = [
                    ...group.querySelectorAll('input[name="court"]'),
                ];
                const selected = children.filter(
                    (court) => court.checked,
                ).length;
                control.hidden = false;
                control.checked = selected === children.length;
                control.indeterminate =
                    selected > 0 && selected < children.length;
            });
        };
        if (toggle.checked)
            courts.forEach((court) => {
                court.checked = true;
            });
        toggle.addEventListener("change", () => {
            courts.forEach((court) => {
                court.checked = toggle.checked;
            });
            update();
        });
        groups.forEach((group) => {
            group
                .querySelector("[data-group-toggle]")
                ?.addEventListener("change", (event) => {
                    group
                        .querySelectorAll('input[name="court"]')
                        .forEach((court) => {
                            court.checked = event.target.checked;
                        });
                    update();
                });
        });
        courts.forEach((court) => court.addEventListener("change", update));
        update();
    });
    const forms = new Set(
        [...root.querySelectorAll("[data-scope-toggle]")].map(
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
                        section.querySelector("[data-scope-toggle]").value,
                    ) && section.querySelector('input[name="court"]:checked'),
            );

            if (!scopes.includes("all_courts") && hasCourtsOutsideScope) {
                event.formData.delete("scope");
                return;
            }

            if (
                scopes.includes("all_courts") ||
                (scopes.includes("higher_courts") &&
                    scopes.includes("other_courts"))
            ) {
                event.formData.set("scope", "all_courts");
            }
            if (form.querySelector("[data-scope-toggle]:checked"))
                event.formData.delete("court");
        }),
    );
}
