npx shadcn@latest add @ss-components/card-01

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

const CardDemo = () => {
return (
<Card className='w-full max-w-md'>
<CardHeader>
<CardTitle>Login to your account</CardTitle>
<CardDescription>Enter your email below to login to your account</CardDescription>
</CardHeader>
<CardContent>
<form>
<div className='flex flex-col gap-6'>
<div className='grid gap-2'>
<Label htmlFor='email'>Email</Label>
<Input id='email' type='email' placeholder='m@example.com' />
</div>
<div className='grid gap-2'>
<div className='flex items-center'>
<Label htmlFor='password'>Password</Label>
<a href='#' className='ml-auto inline-block text-sm underline-offset-4 hover:underline'>
Forgot your password?
</a>
</div>
<Input id='password' type='password' />
</div>
</div>
</form>
<div className='mt-6 flex flex-col gap-2'>
<Button type='submit' className='w-full'>
Login
</Button>
<Button variant='outline' className='w-full'>
Continue with Google
</Button>
</div>
</CardContent>
<CardFooter className='justify-center'>
<div className='text-sm'>
Don&apos;t have an account?{' '}
<a href='#' className='underline underline-offset-4'>
Sign up
</a>
</div>
</CardFooter>
</Card>
)
}

export default CardDemo

Create a shadcn component variant in the codebase.

The codebase should support following:

- Shadcn project structure
- React ^19
- Tailwind CSS ^4
- TypeScript ^5

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind CSS v4 or Typescript.

Shadcn Registry Dependencies:

```bash
npx shadcn@latest add button card input label
```

Copy-paste this file to `components/shadcn-studio/card` folder:

```tsx
card-01.tsx
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'

const CardDemo = () => {
  return (
    <Card className='w-full max-w-md'>
      <CardHeader>
        <CardTitle>Login to your account</CardTitle>
        <CardDescription>Enter your email below to login to your account</CardDescription>
      </CardHeader>
      <CardContent>
        <form>
          <div className='flex flex-col gap-6'>
            <div className='grid gap-2'>
              <Label htmlFor='email'>Email</Label>
              <Input id='email' type='email' placeholder='m@example.com' />
            </div>
            <div className='grid gap-2'>
              <div className='flex items-center'>
                <Label htmlFor='password'>Password</Label>
                <a href='#' className='ml-auto inline-block text-sm underline-offset-4 hover:underline'>
                  Forgot your password?
                </a>
              </div>
              <Input id='password' type='password' />
            </div>
          </div>
        </form>
        <div className='mt-6 flex flex-col gap-2'>
          <Button type='submit' className='w-full'>
            Login
          </Button>
          <Button variant='outline' className='w-full'>
            Continue with Google
          </Button>
        </div>
      </CardContent>
      <CardFooter className='justify-center'>
        <div className='text-sm'>
          Don&apos;t have an account?{' '}
          <a href='#' className='underline underline-offset-4'>
            Sign up
          </a>
        </div>
      </CardFooter>
    </Card>
  )
}

export default CardDemo
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
