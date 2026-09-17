const STORYBOOK_SERVER =
    import.meta.env.STORYBOOK_SERVER || "http://localhost:3000";

export default async function renderComponentHtml(template, macro) {
    const endpointUrl = `${STORYBOOK_SERVER}/storybook-render`;

    const payload = { template, macro };

    const res = await fetch(endpointUrl, {
        method: "POST",
        headers: { "Content-Type": "text/plain;charset=UTF-8" },
        body: JSON.stringify(payload),
    });

    if (!res.ok) {
        const msg = await res.text();
        throw new Error(`Server error: ${msg}`);
    }

    return res.text();
}
