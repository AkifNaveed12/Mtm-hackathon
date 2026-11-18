Create a shadcn component variant in the codebase.

The codebase should support following:

- Shadcn project structure
- React ^19
- Tailwind CSS ^4
- TypeScript ^5

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind CSS v4 or Typescript.

Copy-paste this file to `components/shadcn-studio/typography` folder:

```tsx
typography-06.tsx
const TypographyBlockQuoteDemo = () => {
  return (
    <blockquote className='max-w-2xl border-l-2 pl-6 italic'>
      &quot;In the quiet after repeal, the streets filled with unexpected laughter - small rebellions of joy,&quot; she
      recalled.
    </blockquote>
  )
}

export default TypographyBlockQuoteDemo
```

Instructions to follow:

- Install all listed dependencies and devDependencies using package manager used in the project (npm, yarn, pnpm, etc.)
- Install the required shadcn/ui components using the shadcn CLI using package manager used in the project (npx, pnpm dlx, bunx --bun, etc.)
- Add any CSS variables and styles to the `globals.css` file of this project (just add styles that are listed, no need to add extra styles or variables)
- Create the files with the exact paths provided
- Ensure all imports are correctly configured
- The component should be fully functional and styled according to the provided code
- Now you can use this component in current project

Important: File paths for components, utils, ui, lib, and hooks may vary depending on the project structure. Always check the project's `components.json` file to determine the correct import paths and folder structure. Update all import statements and file paths in the provided code to match the project's configuration before implementing the component.

npx shadcn@latest add @ss-components/typography-06

const TypographyBlockQuoteDemo = () => {
return (
<blockquote className='max-w-2xl border-l-2 pl-6 italic'>
&quot;In the quiet after repeal, the streets filled with unexpected laughter - small rebellions of joy,&quot; she
recalled.
</blockquote>
)
}

export default TypographyBlockQuoteDemo
