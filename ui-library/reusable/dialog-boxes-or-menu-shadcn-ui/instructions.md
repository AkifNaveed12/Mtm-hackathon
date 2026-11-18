npx shadcn@latest add @ss-components/dialog-07

import { Button } from '@/components/ui/button'
import {
Dialog,
DialogClose,
DialogContent,
DialogDescription,
DialogFooter,
DialogHeader,
DialogTitle,
DialogTrigger
} from '@/components/ui/dialog'
import { ScrollArea } from '@/components/ui/scroll-area'
import { ChevronLeftIcon } from 'lucide-react'

const DialogFullScreenDemo = () => {
return (

<Dialog>
<DialogTrigger render={<Button variant='outline' />}>Fullscreen Dialog</DialogTrigger>
<DialogContent className='mb-8 flex h-[calc(100vh-2rem)] min-w-[calc(100vw-2rem)] flex-col justify-between gap-0 p-0'>
<ScrollArea className='flex flex-col justify-between overflow-hidden'>
<DialogHeader className='contents space-y-0 text-left'>
<DialogTitle className='px-6 pt-6'>Product Information</DialogTitle>
<DialogDescription render={<div className='p-6' />}>
<div className='[&_strong]:text-foreground space-y-4 [&_strong]:font-semibold'>
<div className='space-y-1'>
<p>
<strong>Product Name:</strong> SuperTech 2000
</p>
<p>
The SuperTech 2000 is a high-performance device designed for tech enthusiasts and professionals
alike, offering superior functionality and innovative features.
</p>
</div>
<div className='space-y-1'>
<p>
<strong>Specifications:</strong>
</p>
<ul>
<li>Processor: 3.6GHz Octa-Core</li>
<li>Memory: 16GB RAM</li>
<li>Storage: 1TB SSD</li>
<li>Display: 15.6&rdquo; 4K UHD</li>
<li>Battery Life: 12 hours</li>
<li>Weight: 2.1kg</li>
</ul>
</div>
<div className='space-y-1'>
<p>
<strong>Key Features:</strong>
</p>
<ul>
<li>Ultra-fast processing speed for intensive tasks</li>
<li>Long battery life, perfect for on-the-go professionals</li>
<li>Sleek and portable design</li>
<li>Advanced cooling system</li>
<li>Excellent build quality for durability</li>
</ul>
</div>
<div className='space-y-1'>
<p>
<strong>Price:</strong>
</p>
<p>$2,499.99 (Includes 1-year warranty)</p>
</div>
<div className='space-y-1'>
<p>
<strong>Customer Reviews:</strong>
</p>
<p>
&rdquo;Absolutely fantastic device! The performance is exceptional, and it handles all of my design
software without any lag.&rdquo; - John D.
</p>
<p>
&rdquo;Best purchase I&apos;ve made in years. The display quality is stunning, and the battery lasts
all day.&rdquo; - Sarah L.
</p>
<p>
&rdquo;The SuperTech 2000 is a game-changer in the tech industry. Worth every penny!&rdquo; - Emma
W.
</p>
</div>
<div className='space-y-1'>
<p>
<strong>Return Policy:</strong>
</p>
<p>
If you&apos;re not satisfied with your purchase, we offer a 30-day return policy. Return the product
within 30 days of purchase for a full refund.
</p>
</div>
<div className='space-y-1'>
<p>
<strong>Warranty:</strong>
</p>
<p>
Comes with a standard 1-year warranty covering defects in materials and workmanship. Extended
warranty plans are available.
</p>
</div>
</div>
</DialogDescription>
</DialogHeader>
</ScrollArea>
<DialogFooter className='m-0 px-6 sm:justify-end'>
<DialogClose render={<Button variant='outline' />}>
<ChevronLeftIcon />
Back
</DialogClose>
<Button type='button'>Read More</Button>
</DialogFooter>
</DialogContent>
</Dialog>
)
}

export default DialogFullScreenDemo

Create a shadcn component variant in the codebase.

The codebase should support following:

- Shadcn project structure
- React ^19
- Tailwind CSS ^4
- TypeScript ^5

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind CSS v4 or Typescript.

Shadcn Registry Dependencies:

```bash
npx shadcn@latest add button dialog scroll-area
```

Copy-paste this file to `components/shadcn-studio/dialog` folder:

```tsx
dialog-07.tsx
import { Button } from '@/components/ui/button'
import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger
} from '@/components/ui/dialog'
import { ScrollArea } from '@/components/ui/scroll-area'
import { ChevronLeftIcon } from 'lucide-react'

const DialogFullScreenDemo = () => {
  return (
    <Dialog>
      <DialogTrigger render={<Button variant='outline' />}>Fullscreen Dialog</DialogTrigger>
      <DialogContent className='mb-8 flex h-[calc(100vh-2rem)] min-w-[calc(100vw-2rem)] flex-col justify-between gap-0 p-0'>
        <ScrollArea className='flex flex-col justify-between overflow-hidden'>
          <DialogHeader className='contents space-y-0 text-left'>
            <DialogTitle className='px-6 pt-6'>Product Information</DialogTitle>
            <DialogDescription render={<div className='p-6' />}>
              <div className='[&_strong]:text-foreground space-y-4 [&_strong]:font-semibold'>
                <div className='space-y-1'>
                  <p>
                    <strong>Product Name:</strong> SuperTech 2000
                  </p>
                  <p>
                    The SuperTech 2000 is a high-performance device designed for tech enthusiasts and professionals
                    alike, offering superior functionality and innovative features.
                  </p>
                </div>
                <div className='space-y-1'>
                  <p>
                    <strong>Specifications:</strong>
                  </p>
                  <ul>
                    <li>Processor: 3.6GHz Octa-Core</li>
                    <li>Memory: 16GB RAM</li>
                    <li>Storage: 1TB SSD</li>
                    <li>Display: 15.6&rdquo; 4K UHD</li>
                    <li>Battery Life: 12 hours</li>
                    <li>Weight: 2.1kg</li>
                  </ul>
                </div>
                <div className='space-y-1'>
                  <p>
                    <strong>Key Features:</strong>
                  </p>
                  <ul>
                    <li>Ultra-fast processing speed for intensive tasks</li>
                    <li>Long battery life, perfect for on-the-go professionals</li>
                    <li>Sleek and portable design</li>
                    <li>Advanced cooling system</li>
                    <li>Excellent build quality for durability</li>
                  </ul>
                </div>
                <div className='space-y-1'>
                  <p>
                    <strong>Price:</strong>
                  </p>
                  <p>$2,499.99 (Includes 1-year warranty)</p>
                </div>
                <div className='space-y-1'>
                  <p>
                    <strong>Customer Reviews:</strong>
                  </p>
                  <p>
                    &rdquo;Absolutely fantastic device! The performance is exceptional, and it handles all of my design
                    software without any lag.&rdquo; - John D.
                  </p>
                  <p>
                    &rdquo;Best purchase I&apos;ve made in years. The display quality is stunning, and the battery lasts
                    all day.&rdquo; - Sarah L.
                  </p>
                  <p>
                    &rdquo;The SuperTech 2000 is a game-changer in the tech industry. Worth every penny!&rdquo; - Emma
                    W.
                  </p>
                </div>
                <div className='space-y-1'>
                  <p>
                    <strong>Return Policy:</strong>
                  </p>
                  <p>
                    If you&apos;re not satisfied with your purchase, we offer a 30-day return policy. Return the product
                    within 30 days of purchase for a full refund.
                  </p>
                </div>
                <div className='space-y-1'>
                  <p>
                    <strong>Warranty:</strong>
                  </p>
                  <p>
                    Comes with a standard 1-year warranty covering defects in materials and workmanship. Extended
                    warranty plans are available.
                  </p>
                </div>
              </div>
            </DialogDescription>
          </DialogHeader>
        </ScrollArea>
        <DialogFooter className='m-0 px-6 sm:justify-end'>
          <DialogClose render={<Button variant='outline' />}>
            <ChevronLeftIcon />
            Back
          </DialogClose>
          <Button type='button'>Read More</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}

export default DialogFullScreenDemo
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
