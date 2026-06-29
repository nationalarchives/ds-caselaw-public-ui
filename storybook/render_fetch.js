const STORYBOOK_SERVER = "http://localhost:3000";

export default async function renderComponentHtml(template, macro, args = {}) {
    const endpointUrl = `${STORYBOOK_SERVER}/storybook-render`;

    const payload = { template, macro };
    if (macro === "button") {
        if ("label" in args) payload.label = args.label;
        if ("variant" in args) payload.variant = args.variant;
        if ("size" in args) payload.size = args.size;
    }

    console.log("Render request:", payload);

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
