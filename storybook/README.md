#### Adding a New Component

This Storybook setup dynamically renders Jinja macros via Django. Every component MUST have its own \_examples.jinja file Storybook stories always render via the examples macro.

Start creating new components by copying the template folder `ds-caselaw-public-ui/storybook/component-template`

**Important (Read Before Adding a Component)**
_Our jinja components macro files `.jinja` do not render automatically in Storybook, it must be wrapped. Wrapping is not optional - it is how Storybook talks jinja_

- Storybook always renders:
  - `components/examples/banner_examples.jinja`
  - macro: `default`
    **Why:** Storybook can only execute macros that are explicitly exposed through the Django render endpoint. Wrapper macros provide a guaranteed render entry point that Storybook can reliably call.
- `innerHTML` _is intentional and expected_
  **Why:** Storybook receives pre-rendered HTML from Django. Jinja is evaluated server-side, so Storybook must inject the returned HTML string directly.
- No component logic lives in JavaScript
  **Why:**Storybook is a viewer, not a renderer. All rendering logic must remain in Jinja to match production output.
- Do not render `banner()` directly from Storybook
  **Why:** In this setup, base macros defined in component files (like `banner()`) do not reliably render when called directly by Storybook. They must be invoked through a wrapper macro in an examples file to ensure Django renders them correctly.
- Do not skip the `_examples.jinja` file held in this folder `components/examples`
  **Why:** The examples file is required to bridge Storybook and Jinja. Without it, Storybook cannot consistently render component macros, which is why base macros appeared “broken” until a wrapper was introduced.
- Do not put macro `macro default()` or `*_examples()` inside `banner.jinja` they are only to be used in the wrapper for Storybook.
  **Why** `banner.jinja` is production code and must remain framework-agnostic. Storybook-specific wrapper macros exist solely to make Jinja renderable by Storybook and must live in the `_examples.jinja` file.
- Every component must include an MDX file
  **Why** MDX adds in the menu the "Jinja Macros" documentation so this is added to storybook \*.
