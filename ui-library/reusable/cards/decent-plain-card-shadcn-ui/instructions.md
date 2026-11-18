Create a shadcn component variant in the codebase.

The codebase should support following:

- Shadcn project structure
- React ^19
- Tailwind CSS ^4
- TypeScript ^5

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind CSS v4 or Typescript.

Shadcn Registry Dependencies:

```bash
npx shadcn@latest add button card
```

Copy-paste this file to `components/shadcn-studio/card` folder:

```tsx
card-05.tsx
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardDescription, CardTitle, CardFooter } from '@/components/ui/card'

const CardTopImageDemo = () => {
  return (
    <Card className='max-w-md pt-0'>
      <CardContent className='px-0'>
        <img
          src='https://cdn.shadcnstudio.com/ss-assets/components/card/image-2.png?height=280&format=auto'
          alt='Banner'
          className='aspect-video h-70 rounded-t-xl object-cover'
        />
      </CardContent>
      <CardHeader>
        <CardTitle>Ethereal Swirl Gradient</CardTitle>
        <CardDescription>Smooth, flowing gradients blending rich reds and blues in an abstract swirl.</CardDescription>
      </CardHeader>
      <CardFooter className='gap-3 max-sm:flex-col max-sm:items-stretch'>
        <Button>Explore More</Button>
        <Button variant={'outline'}>Download Now</Button>
      </CardFooter>
    </Card>
  )
}

export default CardTopImageDemo
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

npx shadcn@latest add @ss-components/card-05
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardDescription, CardTitle, CardFooter } from '@/components/ui/card'

const CardTopImageDemo = () => {
return (
<Card className='max-w-md pt-0'>
<CardContent className='px-0'>
<img
          src='https://cdn.shadcnstudio.com/ss-assets/components/card/image-2.png?height=280&format=auto'
          alt='Banner'
          className='aspect-video h-70 rounded-t-xl object-cover'
        />
</CardContent>
<CardHeader>
<CardTitle>Ethereal Swirl Gradient</CardTitle>
<CardDescription>Smooth, flowing gradients blending rich reds and blues in an abstract swirl.</CardDescription>
</CardHeader>
<CardFooter className='gap-3 max-sm:flex-col max-sm:items-stretch'>
<Button>Explore More</Button>
<Button variant={'outline'}>Download Now</Button>
</CardFooter>
</Card>
)
}

export default CardTopImageDemo
