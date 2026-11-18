npx shadcn@latest add @ss-components/drawer-14

import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import { Drawer, DrawerContent, DrawerHeader, DrawerTitle, DrawerTrigger } from '@/components/ui/drawer'
import { Separator } from '@/components/ui/separator'
import { UserIcon, BadgeCheckIcon } from 'lucide-react'

const DrawerProfile = () => {
return (
<Drawer direction='right'>
<DrawerTrigger asChild>
<Button variant='outline'>
<UserIcon />{' '}
Profile
</Button>
</DrawerTrigger>
<DrawerContent>
<DrawerHeader>
<DrawerTitle>Contact Details</DrawerTitle>
</DrawerHeader>

<div className='no-scrollbar h-full overflow-y-auto'>
<div className='bg-muted p-2'>
<p className='text-muted-foreground ml-4 uppercase'>Contact</p>
</div>
<div className='flex flex-col items-center justify-center gap-4 p-6'>
<div className='relative w-fit'>
<Avatar className='size-14'>
<AvatarImage src='https://cdn.shadcnstudio.com/ss-assets/avatar/avatar-1.png' alt='Hallie Richards' />
<AvatarFallback>HR</AvatarFallback>
</Avatar>
<span className='absolute -top-1.5 -right-1.5'>
<span className='sr-only'>Verified</span>
<BadgeCheckIcon className='text-background size-6 fill-sky-500' />
</span>
</div>
<div className='space-y-2 text-center'>
<h4 className='text-lg font-medium'>Matthew Johnson</h4>
<p>A-8486214</p>
</div>
</div>
<div className='bg-muted p-2'>
<p className='text-muted-foreground ml-4 uppercase'>Information</p>
</div>
<div className='space-y-3 p-4'>
<div className='space-y-1'>
<div className='text-muted-foreground uppercase'>Full Name</div>
<div className='text-sm'>Matthew Johnson</div>
</div>
<Separator />
<div className='space-y-1'>
<div className='text-muted-foreground uppercase'>Country</div>
<div className='text-sm'>USA</div>
</div>
<Separator />
<div className='space-y-1'>
<div className='text-muted-foreground uppercase'>Role</div>
<div className='text-sm'>Developer</div>
</div>
<Separator />
<div className='space-y-1'>
<div className='text-muted-foreground uppercase'>Email</div>
<div className='text-sm'>matthew@shadcnstudio.com</div>
</div>
<Separator />
<div className='space-y-1'>
<div className='text-muted-foreground uppercase'>Phone number</div>
<div className='text-sm'>+1 548 564 62 28</div>
</div>
</div>
<div className='bg-muted p-2'>
<p className='text-muted-foreground ml-4 uppercase'>Teams</p>
</div>
<div className='space-y-3 p-4'>
<div className='space-y-1'>
<div className='text-muted-foreground uppercase'>Backend Developer</div>
<div className='text-sm'>126 Members</div>
</div>
<Separator />
<div className='space-y-1'>
<div className='text-muted-foreground uppercase'>React Developer</div>
<div className='text-sm'>98 Members</div>
</div>
</div>
</div>
</DrawerContent>
</Drawer>
)
}

export default DrawerProfile

Create a shadcn component variant in the codebase.

The codebase should support following:

- Shadcn project structure
- React ^19
- Tailwind CSS ^4
- TypeScript ^5

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind CSS v4 or Typescript.

Shadcn Registry Dependencies:

```bash
npx shadcn@latest add button drawer separator avatar
```

Copy-paste this file to `components/shadcn-studio/drawer` folder:

```tsx
drawer-14.tsx
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import { Drawer, DrawerContent, DrawerHeader, DrawerTitle, DrawerTrigger } from '@/components/ui/drawer'
import { Separator } from '@/components/ui/separator'
import { UserIcon, BadgeCheckIcon } from 'lucide-react'

const DrawerProfile = () => {
  return (
    <Drawer direction='right'>
      <DrawerTrigger asChild>
        <Button variant='outline'>
          <UserIcon />{' '}
          Profile
        </Button>
      </DrawerTrigger>
      <DrawerContent>
        <DrawerHeader>
          <DrawerTitle>Contact Details</DrawerTitle>
        </DrawerHeader>
        <div className='no-scrollbar h-full overflow-y-auto'>
          <div className='bg-muted p-2'>
            <p className='text-muted-foreground ml-4 uppercase'>Contact</p>
          </div>
          <div className='flex flex-col items-center justify-center gap-4 p-6'>
            <div className='relative w-fit'>
              <Avatar className='size-14'>
                <AvatarImage src='https://cdn.shadcnstudio.com/ss-assets/avatar/avatar-1.png' alt='Hallie Richards' />
                <AvatarFallback>HR</AvatarFallback>
              </Avatar>
              <span className='absolute -top-1.5 -right-1.5'>
                <span className='sr-only'>Verified</span>
                <BadgeCheckIcon className='text-background size-6 fill-sky-500' />
              </span>
            </div>
            <div className='space-y-2 text-center'>
              <h4 className='text-lg font-medium'>Matthew Johnson</h4>
              <p>A-8486214</p>
            </div>
          </div>
          <div className='bg-muted p-2'>
            <p className='text-muted-foreground ml-4 uppercase'>Information</p>
          </div>
          <div className='space-y-3 p-4'>
            <div className='space-y-1'>
              <div className='text-muted-foreground uppercase'>Full Name</div>
              <div className='text-sm'>Matthew Johnson</div>
            </div>
            <Separator />
            <div className='space-y-1'>
              <div className='text-muted-foreground uppercase'>Country</div>
              <div className='text-sm'>USA</div>
            </div>
            <Separator />
            <div className='space-y-1'>
              <div className='text-muted-foreground uppercase'>Role</div>
              <div className='text-sm'>Developer</div>
            </div>
            <Separator />
            <div className='space-y-1'>
              <div className='text-muted-foreground uppercase'>Email</div>
              <div className='text-sm'>matthew@shadcnstudio.com</div>
            </div>
            <Separator />
            <div className='space-y-1'>
              <div className='text-muted-foreground uppercase'>Phone number</div>
              <div className='text-sm'>+1 548 564 62 28</div>
            </div>
          </div>
          <div className='bg-muted p-2'>
            <p className='text-muted-foreground ml-4 uppercase'>Teams</p>
          </div>
          <div className='space-y-3 p-4'>
            <div className='space-y-1'>
              <div className='text-muted-foreground uppercase'>Backend Developer</div>
              <div className='text-sm'>126 Members</div>
            </div>
            <Separator />
            <div className='space-y-1'>
              <div className='text-muted-foreground uppercase'>React Developer</div>
              <div className='text-sm'>98 Members</div>
            </div>
          </div>
        </div>
      </DrawerContent>
    </Drawer>
  )
}

export default DrawerProfile
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
