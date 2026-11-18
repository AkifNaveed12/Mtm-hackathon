npx shadcn@latest add @ss-components/dialog-13

import { useId } from 'react'

import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import {
Dialog,
DialogContent,
DialogDescription,
DialogFooter,
DialogHeader,
DialogTitle,
DialogTrigger
} from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

const DialogSignUpDemo = () => {
const id = useId()

return (
<Dialog>
<form>
<DialogTrigger render={<Button variant='outline' />}>Sign Up</DialogTrigger>
<DialogContent className='to-card bg-linear-to-b from-green-100 to-40% bg-size-[100%_101%] dark:from-green-900'>
<DialogHeader className='items-center'>
<DialogTitle>Sign Up</DialogTitle>
<DialogDescription>Start your 60-day free trial now.</DialogDescription>
</DialogHeader>
<form className='flex flex-col gap-4'>
<div className='grid grid-cols-2 gap-4'>
<div className='grid gap-3'>
<Label htmlFor='first-name'>First Name</Label>
<Input id='first-name' name='firstname' placeholder='John' />
</div>
<div className='grid gap-3'>
<Label htmlFor='last-name'>Last Name</Label>
<Input id='last-name' name='lastname' placeholder='Doe' />
</div>
</div>
<div className='grid gap-3'>
<Label htmlFor='email'>Email</Label>
<Input type='email' id='email' name='useremail' placeholder='example@gmail.com' />
</div>
<div className='grid gap-3'>
<Label htmlFor='password'>Password</Label>
<Input type='password' id='password' name='userpassword' placeholder='Password' />
</div>
<div className='flex items-center gap-2'>
<Checkbox
                id={id}
                className='focus-visible:ring-green-600/20 data-checked:border-green-600 data-checked:bg-green-600 dark:text-white dark:focus-visible:ring-green-400/40 dark:data-checked:border-green-400 dark:data-checked:bg-green-400'
                defaultChecked
              />
<Label htmlFor={id} className='gap-1'>
I agree with
<a href='#' className='underline hover:no-underline'>
condition
</a>
and
<a href='#' className='underline hover:no-underline'>
privacy policy
</a>
</Label>
</div>
</form>
<DialogFooter className='pt-4 sm:flex-col'>
<Button className='bg-green-600 text-white hover:bg-green-600 focus-visible:ring-green-600 dark:bg-green-400 dark:hover:bg-green-400 dark:focus-visible:ring-green-400'>
Start your trial
</Button>
<div className='before:bg-border after:bg-border flex items-center gap-4 before:h-px before:flex-1 after:h-px after:flex-1'>
<span className='text-muted-foreground text-xs'>Or</span>
</div>
<Button variant='outline'>
<img
                src='https://cdn.shadcnstudio.com/ss-assets/brand-logo/google-icon.png?width=20&height=20&format=auto'
                alt='Google Icon'
                className='size-5'
              />
<span className='flex justify-center'>Continue with Google</span>
</Button>
</DialogFooter>
</DialogContent>
</form>
</Dialog>
)
}

export default DialogSignUpDemo

Create a shadcn component variant in the codebase.

The codebase should support following:

- Shadcn project structure
- React ^19
- Tailwind CSS ^4
- TypeScript ^5

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind CSS v4 or Typescript.

Shadcn Registry Dependencies:

```bash
npx shadcn@latest add button checkbox dialog input label
```

Copy-paste this file to `components/shadcn-studio/dialog` folder:

```tsx
dialog-13.tsx
import { useId } from 'react'

import { Button } from '@/components/ui/button'
import { Checkbox } from '@/components/ui/checkbox'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger
} from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

const DialogSignUpDemo = () => {
  const id = useId()

  return (
    <Dialog>
      <form>
        <DialogTrigger render={<Button variant='outline' />}>Sign Up</DialogTrigger>
        <DialogContent className='to-card bg-linear-to-b from-green-100 to-40% bg-size-[100%_101%] dark:from-green-900'>
          <DialogHeader className='items-center'>
            <DialogTitle>Sign Up</DialogTitle>
            <DialogDescription>Start your 60-day free trial now.</DialogDescription>
          </DialogHeader>
          <form className='flex flex-col gap-4'>
            <div className='grid grid-cols-2 gap-4'>
              <div className='grid gap-3'>
                <Label htmlFor='first-name'>First Name</Label>
                <Input id='first-name' name='firstname' placeholder='John' />
              </div>
              <div className='grid gap-3'>
                <Label htmlFor='last-name'>Last Name</Label>
                <Input id='last-name' name='lastname' placeholder='Doe' />
              </div>
            </div>
            <div className='grid gap-3'>
              <Label htmlFor='email'>Email</Label>
              <Input type='email' id='email' name='useremail' placeholder='example@gmail.com' />
            </div>
            <div className='grid gap-3'>
              <Label htmlFor='password'>Password</Label>
              <Input type='password' id='password' name='userpassword' placeholder='Password' />
            </div>
            <div className='flex items-center gap-2'>
              <Checkbox
                id={id}
                className='focus-visible:ring-green-600/20 data-checked:border-green-600 data-checked:bg-green-600 dark:text-white dark:focus-visible:ring-green-400/40 dark:data-checked:border-green-400 dark:data-checked:bg-green-400'
                defaultChecked
              />
              <Label htmlFor={id} className='gap-1'>
                I agree with
                <a href='#' className='underline hover:no-underline'>
                  condition
                </a>
                and
                <a href='#' className='underline hover:no-underline'>
                  privacy policy
                </a>
              </Label>
            </div>
          </form>
          <DialogFooter className='pt-4 sm:flex-col'>
            <Button className='bg-green-600 text-white hover:bg-green-600 focus-visible:ring-green-600 dark:bg-green-400 dark:hover:bg-green-400 dark:focus-visible:ring-green-400'>
              Start your trial
            </Button>
            <div className='before:bg-border after:bg-border flex items-center gap-4 before:h-px before:flex-1 after:h-px after:flex-1'>
              <span className='text-muted-foreground text-xs'>Or</span>
            </div>
            <Button variant='outline'>
              <img
                src='https://cdn.shadcnstudio.com/ss-assets/brand-logo/google-icon.png?width=20&height=20&format=auto'
                alt='Google Icon'
                className='size-5'
              />
              <span className='flex justify-center'>Continue with Google</span>
            </Button>
          </DialogFooter>
        </DialogContent>
      </form>
    </Dialog>
  )
}

export default DialogSignUpDemo
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
