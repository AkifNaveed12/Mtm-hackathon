Create a shadcn component variant in the codebase.

The codebase should support following:

- Shadcn project structure
- React ^19
- Tailwind CSS ^4
- TypeScript ^5

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind CSS v4 or Typescript.

Shadcn Registry Dependencies:

```bash
npx shadcn@latest add collapsible
```

Copy-paste this file to `components/shadcn-studio/collapsible` folder:

```tsx
collapsible-06.tsx
'use client'

import { useState } from 'react'

import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible'

const CollapsibleShowMoreDemo = () => {
  const [isTrackOrderOpen, setIsTrackOrderOpen] = useState(true)
  const [isCancelOrderOpen, setIsCancelOrderOpen] = useState(false)

  return (
    <div className='w-full space-y-4'>
      <div className='space-y-2'>
        <p className='font-medium'>How can I track my order?</p>
        <Collapsible open={isTrackOrderOpen} onOpenChange={setIsTrackOrderOpen} className='space-y-2'>
          <CollapsibleContent>
            <p className='text-sm'>
              To track your order, simply log in to your account and navigate to the order history section. You&apos;ll
              find detailed information about your order status and tracking number there.
            </p>
          </CollapsibleContent>
          <CollapsibleTrigger>
            <span className='text-muted-foreground text-sm underline'>
              {isTrackOrderOpen ? 'Hide answer' : 'Show answer'}
            </span>
          </CollapsibleTrigger>
        </Collapsible>
      </div>
      <div className='space-y-2'>
        <p className='font-medium'>Can I cancel my order?</p>
        <Collapsible open={isCancelOrderOpen} onOpenChange={setIsCancelOrderOpen} className='space-y-2'>
          <CollapsibleContent>
            <p className='text-sm'>
              Scheduled delivery orders can be cancelled 72 hours prior to your selected delivery date for full refund.
            </p>
          </CollapsibleContent>
          <CollapsibleTrigger>
            <span className='text-muted-foreground text-sm underline'>
              {isCancelOrderOpen ? 'Hide answer' : 'Show answer'}
            </span>
          </CollapsibleTrigger>
        </Collapsible>
      </div>
    </div>
  )
}

export default CollapsibleShowMoreDemo
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

npx shadcn@latest add @ss-components/collapsible-06
'use client'

import { useState } from 'react'

import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible'

const CollapsibleShowMoreDemo = () => {
const [isTrackOrderOpen, setIsTrackOrderOpen] = useState(true)
const [isCancelOrderOpen, setIsCancelOrderOpen] = useState(false)

return (
<div className='w-full space-y-4'>
<div className='space-y-2'>
<p className='font-medium'>How can I track my order?</p>
<Collapsible open={isTrackOrderOpen} onOpenChange={setIsTrackOrderOpen} className='space-y-2'>
<CollapsibleContent>
<p className='text-sm'>
To track your order, simply log in to your account and navigate to the order history section. You&apos;ll
find detailed information about your order status and tracking number there.
</p>
</CollapsibleContent>
<CollapsibleTrigger>
<span className='text-muted-foreground text-sm underline'>
{isTrackOrderOpen ? 'Hide answer' : 'Show answer'}
</span>
</CollapsibleTrigger>
</Collapsible>
</div>
<div className='space-y-2'>
<p className='font-medium'>Can I cancel my order?</p>
<Collapsible open={isCancelOrderOpen} onOpenChange={setIsCancelOrderOpen} className='space-y-2'>
<CollapsibleContent>
<p className='text-sm'>
Scheduled delivery orders can be cancelled 72 hours prior to your selected delivery date for full refund.
</p>
</CollapsibleContent>
<CollapsibleTrigger>
<span className='text-muted-foreground text-sm underline'>
{isCancelOrderOpen ? 'Hide answer' : 'Show answer'}
</span>
</CollapsibleTrigger>
</Collapsible>
</div>
</div>
)
}

export default CollapsibleShowMoreDemo
