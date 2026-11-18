npx shadcn@latest add @ss-components/drawer-05

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
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'

const DrawerWithSides = () => {
return (
<Drawer direction='right'>
<DrawerTrigger asChild>
<Button variant='outline'>Form</Button>
</DrawerTrigger>
<DrawerContent>
<DrawerHeader>
<DrawerTitle>Sign In</DrawerTitle>
<DrawerDescription>Fill the form to get full access</DrawerDescription>
</DrawerHeader>

<div className='grid flex-1 auto-rows-min gap-6 px-4'>
<div className='grid gap-3'>
<Label htmlFor='drawer-demo-name'>Full Name</Label>
<Input id='drawer-demo-name' placeholder='John Doe' />
</div>
<div className='grid gap-3'>
<Label htmlFor='drawer-demo-email'>Email</Label>
<Input id='drawer-demo-email' placeholder='john.doe@example.com' />
</div>
<div className='grid gap-3'>
<Label htmlFor='drawer-demo-address'>Address</Label>
<Input id='drawer-demo-address' placeholder='123 Main St' />
</div>
<div className='grid gap-3'>
<Label htmlFor='drawer-demo-description'>Description</Label>
<Textarea id='drawer-demo-description' placeholder='Enter a description' />
</div>
</div>
<DrawerFooter>
<Button>Submit</Button>
<DrawerClose asChild>
<Button variant='outline'>Cancel</Button>
</DrawerClose>
</DrawerFooter>
</DrawerContent>
</Drawer>
)
}

export default DrawerWithSides

Create a shadcn component variant in the codebase.

The codebase should support following:

- Shadcn project structure
- React ^19
- Tailwind CSS ^4
- TypeScript ^5

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind CSS v4 or Typescript.

Shadcn Registry Dependencies:

```bash
npx shadcn@latest add button drawer input label textarea
```

Copy-paste this file to `components/shadcn-studio/drawer` folder:

```tsx
drawer-05.tsx
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
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'

const DrawerWithSides = () => {
  return (
    <Drawer direction='right'>
      <DrawerTrigger asChild>
        <Button variant='outline'>Form</Button>
      </DrawerTrigger>
      <DrawerContent>
        <DrawerHeader>
          <DrawerTitle>Sign In</DrawerTitle>
          <DrawerDescription>Fill the form to get full access</DrawerDescription>
        </DrawerHeader>
        <div className='grid flex-1 auto-rows-min gap-6 px-4'>
          <div className='grid gap-3'>
            <Label htmlFor='drawer-demo-name'>Full Name</Label>
            <Input id='drawer-demo-name' placeholder='John Doe' />
          </div>
          <div className='grid gap-3'>
            <Label htmlFor='drawer-demo-email'>Email</Label>
            <Input id='drawer-demo-email' placeholder='john.doe@example.com' />
          </div>
          <div className='grid gap-3'>
            <Label htmlFor='drawer-demo-address'>Address</Label>
            <Input id='drawer-demo-address' placeholder='123 Main St' />
          </div>
          <div className='grid gap-3'>
            <Label htmlFor='drawer-demo-description'>Description</Label>
            <Textarea id='drawer-demo-description' placeholder='Enter a description' />
          </div>
        </div>
        <DrawerFooter>
          <Button>Submit</Button>
          <DrawerClose asChild>
            <Button variant='outline'>Cancel</Button>
          </DrawerClose>
        </DrawerFooter>
      </DrawerContent>
    </Drawer>
  )
}

export default DrawerWithSides
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
