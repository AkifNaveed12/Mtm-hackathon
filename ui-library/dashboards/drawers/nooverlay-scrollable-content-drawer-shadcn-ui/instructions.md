npx shadcn@latest add @ss-components/drawer-06

import { Button } from '@/components/ui/button'
import {
Drawer,
DrawerClose,
DrawerContent,
DrawerDescription,
DrawerFooter,
DrawerHeader,
DrawerTitle,
DrawerTrigger
} from '@/components/ui/drawer'
import { ArrowRightIcon } from 'lucide-react'

const DrawerNoOverlay = () => {
return (
<Drawer direction='right' modal={false}>
<DrawerTrigger asChild>
<Button variant='outline'>No Overlay</Button>
</DrawerTrigger>
<DrawerContent>
<DrawerHeader>
<DrawerTitle>Shadcn Studio</DrawerTitle>
<DrawerDescription>
Accelerate your project development with ready-to-use, & customizable 1000+ Shadcn UI Components, Blocks, UI
Kit, Boilerplate, Templates & Themes.
</DrawerDescription>
</DrawerHeader>

<div className='no-scrollbar overflow-y-auto px-4'>
{Array.from({ length: 10 }).map((\_, index) => (
<p key={index} className='mb-4'>
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et
dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex
ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt
mollit anim id est laborum.
</p>
))}
</div>
<DrawerFooter>
<Button>
Learn more{' '}
<ArrowRightIcon />
</Button>
<DrawerClose asChild>
<Button variant='outline'>Got it !</Button>
</DrawerClose>
</DrawerFooter>
</DrawerContent>
</Drawer>
)
}

export default DrawerNoOverlay
Create a shadcn component variant in the codebase.

The codebase should support following:

- Shadcn project structure
- React ^19
- Tailwind CSS ^4
- TypeScript ^5

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind CSS v4 or Typescript.

Shadcn Registry Dependencies:

```bash
npx shadcn@latest add button drawer
```

Copy-paste this file to `components/shadcn-studio/drawer` folder:

```tsx
drawer-06.tsx
import { Button } from '@/components/ui/button'
import {
  Drawer,
  DrawerClose,
  DrawerContent,
  DrawerDescription,
  DrawerFooter,
  DrawerHeader,
  DrawerTitle,
  DrawerTrigger
} from '@/components/ui/drawer'
import { ArrowRightIcon } from 'lucide-react'

const DrawerNoOverlay = () => {
  return (
    <Drawer direction='right' modal={false}>
      <DrawerTrigger asChild>
        <Button variant='outline'>No Overlay</Button>
      </DrawerTrigger>
      <DrawerContent>
        <DrawerHeader>
          <DrawerTitle>Shadcn Studio</DrawerTitle>
          <DrawerDescription>
            Accelerate your project development with ready-to-use, & customizable 1000+ Shadcn UI Components, Blocks, UI
            Kit, Boilerplate, Templates & Themes.
          </DrawerDescription>
        </DrawerHeader>
        <div className='no-scrollbar overflow-y-auto px-4'>
          {Array.from({ length: 10 }).map((_, index) => (
            <p key={index} className='mb-4'>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et
              dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex
              ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
              fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt
              mollit anim id est laborum.
            </p>
          ))}
        </div>
        <DrawerFooter>
          <Button>
            Learn more{' '}
            <ArrowRightIcon />
          </Button>
          <DrawerClose asChild>
            <Button variant='outline'>Got it !</Button>
          </DrawerClose>
        </DrawerFooter>
      </DrawerContent>
    </Drawer>
  )
}

export default DrawerNoOverlay
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
