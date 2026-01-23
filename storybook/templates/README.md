#### Component Starter Template

- A generic \_examples.jinja wrapper
- A generic .stories.js
- A generic .mdx
- The component macro itself cannot be generic, but everything around it can be.
- This folder is documentation + starter code templates only

**1. `component.jinja` (starter template)**

What to do:

- Rename `component`, `component()` for example banner
- Important- the title in the stories.js file must be exact same as the .mdx file. For example in a banner.stories.js `title: "Components/Banner Examples"` must be the same name as the banner .mdx file title `<Meta title="Components/Banner Examples/Jinja Macros"` />`
- Replace markup + any div classes you already use in code base
- Rename `<component>.jinja` file

Once this is done move `<component>`file to this location: `ds-caselaw-public-ui/ds_judgements_public_ui/templates/components/<component>.jinja`

**2. `component_examples.jinja` (wrapper template)**

What to do:

- Update `component.jinja` to match your renamed file
- Optional heading if needed
- Does not move this macro into the component file
- Rename `component_examples`file to match `<component>` from renamed file

Once this is done move `<component>_examples`file to this location: `ds-caselaw-public-ui/ds_judgements_public_ui/templates/components/examples/<component>_examples.jinja`

**3. `component.stories.js` (Storybook template)**

What to do:

- Replace `<Component Name>` with the exact name of file you named in _step 1_ and moved to this location: `ds-caselaw-public-ui/ds_judgements_public_ui/templates/components/`
- Replace `<component>` with the exact name of file you named in _step 2_ and moved to this location `ds-caselaw-public-ui/ds_judgements_public_ui/templates/components/examples/<component>_examples.jinja`
- Rename `<component>_stories.js`file to match `<component>` from renamed file

** `component.mdx` (Storybook mdx template)**

What to do:

- Update `<ExportedConstName>` to the const you exported in your .stories.js file in _step 3_ which is `Default` based on `export const Default = {...}`
- Update `<DisplayNameInStorybook>` it is the label shown in Storybook’s UI best to match `<ExportedConstName>`
- Update `<component>_stories.js`file to match that file name
- Replace `<Component Name>` with the exact name of file you named in _step 1_ and moved to this location: `ds-caselaw-public-ui/ds_judgements_public_ui/templates/components/`
- Rename file `<component>.mdx`file to `Macro<Component>.mdx` so the `<Component>` matches same names created in step 1, 2 and 3 so files have same name for example `banner.jinja`, `banner_examples.jinja`, `banner.stories.js`, `MacroBanner.mdx`

Once this is done move `<component>.mdx`file to this location: `ds-caselaw-public-ui/storybook/stories/Macro<Component>.mdx`
