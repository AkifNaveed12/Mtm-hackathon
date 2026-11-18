npx shadcn@latest add @ss-components/navigation-menu-01

import Link from 'next/link'

import {
NavigationMenu,
NavigationMenuContent,
NavigationMenuItem,
NavigationMenuLink,
NavigationMenuList,
NavigationMenuTrigger
} from '@/components/ui/navigation-menu'

const NavigationMenuDemo = () => {
return (

<div className='flex items-center justify-center'>
<NavigationMenu>
<NavigationMenuList>
<NavigationMenuItem>
<NavigationMenuTrigger className='[&>svg]:size-4'>Components</NavigationMenuTrigger>
<NavigationMenuContent>
<ul className='w-80'>
<li>
<NavigationMenuLink render={<Link href='#' />}>
<div className='flex flex-col px-1'>
<div className='font-medium'>Alert Dialog</div>
<div className='text-muted-foreground text-sm'>
A modal dialog that interrupts the user with important content and expects a response.
</div>
</div>
</NavigationMenuLink>
</li>
<li>
<NavigationMenuLink render={<Link href='#' />}>
<div className='flex flex-col px-1'>
<div className='font-medium'>Hover Card</div>
<div className='text-muted-foreground text-sm'>
For sighted users to preview content available behind a link.
</div>
</div>
</NavigationMenuLink>
</li>
</ul>
</NavigationMenuContent>
</NavigationMenuItem>
</NavigationMenuList>
</NavigationMenu>
</div>
)
}

export default NavigationMenuDemo

Create a shadcn component variant in the codebase.

The codebase should support following:

- Shadcn project structure
- React ^19
- Tailwind CSS ^4
- TypeScript ^5

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind CSS v4 or Typescript.

Shadcn Registry Dependencies:

```bash
npx shadcn@latest add navigation-menu
```

Copy-paste this file to `components/shadcn-studio/navigation-menu` folder:

```tsx
navigation-menu-01.tsx
import Link from 'next/link'

import {
  NavigationMenu,
  NavigationMenuContent,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  NavigationMenuTrigger
} from '@/components/ui/navigation-menu'

const NavigationMenuDemo = () => {
  return (
    <div className='flex items-center justify-center'>
      <NavigationMenu>
        <NavigationMenuList>
          <NavigationMenuItem>
            <NavigationMenuTrigger className='[&>svg]:size-4'>Components</NavigationMenuTrigger>
            <NavigationMenuContent>
              <ul className='w-80'>
                <li>
                  <NavigationMenuLink render={<Link href='#' />}>
                    <div className='flex flex-col px-1'>
                      <div className='font-medium'>Alert Dialog</div>
                      <div className='text-muted-foreground text-sm'>
                        A modal dialog that interrupts the user with important content and expects a response.
                      </div>
                    </div>
                  </NavigationMenuLink>
                </li>
                <li>
                  <NavigationMenuLink render={<Link href='#' />}>
                    <div className='flex flex-col px-1'>
                      <div className='font-medium'>Hover Card</div>
                      <div className='text-muted-foreground text-sm'>
                        For sighted users to preview content available behind a link.
                      </div>
                    </div>
                  </NavigationMenuLink>
                </li>
              </ul>
            </NavigationMenuContent>
          </NavigationMenuItem>
        </NavigationMenuList>
      </NavigationMenu>
    </div>
  )
}

export default NavigationMenuDemo
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
