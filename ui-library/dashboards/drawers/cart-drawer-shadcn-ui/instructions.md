npx shadcn@latest add @ss-components/drawer-13

import { Button } from '@/components/ui/button'
import {
Drawer,
DrawerClose,
DrawerContent,
DrawerFooter,
DrawerHeader,
DrawerTitle,
DrawerTrigger
} from '@/components/ui/drawer'
import { Separator } from '@/components/ui/separator'
import { ShoppingCartIcon, Trash2Icon, ArrowRightIcon } from 'lucide-react'

type CartItem = {
id: string
name: string
description: string
price: string
image: string
}

interface DrawerCartProps {
items?: CartItem[]
}

const defaultItems: CartItem[] = [
{
id: '1',
name: 'Polarised sunglasses',
description: 'Polarized sunglasses with UV protection',
price: '$199.99',
image: 'https://cdn.shadcnstudio.com/ss-assets/blocks/ecommerce/shopping-cart/image-7.png'
},
{
id: '2',
name: 'Lyocell-blend bucket hat',
description: 'Bucket hat in woven fabric made from a lyocell and nylon blend.',
price: '$19',
image: 'https://cdn.shadcnstudio.com/ss-assets/blocks/ecommerce/shopping-cart/image-6.png'
},
{
id: '3',
name: 'Regular Fit Polo shirt',
description: 'Regular fit polo shirt in breathable fabric.',
price: '$29',
image: 'https://cdn.shadcnstudio.com/ss-assets/blocks/ecommerce/shopping-cart/image-5.png'
}
]

const DrawerCart = ({ items = defaultItems }: DrawerCartProps) => {
return (
<Drawer direction='right'>
<DrawerTrigger asChild>
<Button variant='outline'>
<ShoppingCartIcon />{' '}
Cart
</Button>
</DrawerTrigger>
<DrawerContent>
<DrawerHeader>
<DrawerTitle>Cart</DrawerTitle>
</DrawerHeader>

<div className='no-scrollbar space-y-4 overflow-y-auto px-4'>
{items.map((item, index) => (
<div key={item.id}>
{index > 0 && <Separator key={`sep-${item.id}`} className='my-4' />}
<div key={item.id} className='space-y-4'>
<div className='flex items-start gap-4'>
<div className='size-18 overflow-hidden rounded-lg border'>
<img src={item.image} alt={item.name} />
</div>
<div className='flex-1 space-y-2'>
<h4 className='font-medium'>{item.name}</h4>
<p className='text-muted-foreground text-sm'>{item.description}</p>
<p className='font-medium'>{item.price}</p>
</div>
</div>
<Button
                  variant='outline'
                  className='border-destructive text-destructive hover:bg-destructive/10 hover:text-destructive focus-visible:border-destructive focus-visible:ring-destructive/20 dark:focus-visible:ring-destructive/40 w-full'
                >
<Trash2Icon />
Remove
</Button>
</div>
</div>
))}
<div className='my-4 space-y-2'>
<div className='flex justify-between'>
<p className='text-muted-foreground'>Subtotal</p>
<p>$247.99</p>
</div>
<div className='flex justify-between'>
<p className='text-muted-foreground'>Shipping</p>
<p>$10.00</p>
</div>
<Separator />
<div className='flex justify-between'>
<p className='font-medium'>Total</p>
<p className='font-medium'>$257.99</p>
</div>
</div>
</div>
<DrawerFooter>
<Button>
Checkout{' '}
<ArrowRightIcon />
</Button>
<DrawerClose asChild>
<Button variant='outline'>Continue Shopping</Button>
</DrawerClose>
</DrawerFooter>
</DrawerContent>
</Drawer>
)
}

export default DrawerCart

Create a shadcn component variant in the codebase.

The codebase should support following:

- Shadcn project structure
- React ^19
- Tailwind CSS ^4
- TypeScript ^5

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind CSS v4 or Typescript.

Shadcn Registry Dependencies:

```bash
npx shadcn@latest add button drawer separator
```

Copy-paste this file to `components/shadcn-studio/drawer` folder:

```tsx
drawer-13.tsx
import { Button } from '@/components/ui/button'
import {
  Drawer,
  DrawerClose,
  DrawerContent,
  DrawerFooter,
  DrawerHeader,
  DrawerTitle,
  DrawerTrigger
} from '@/components/ui/drawer'
import { Separator } from '@/components/ui/separator'
import { ShoppingCartIcon, Trash2Icon, ArrowRightIcon } from 'lucide-react'

type CartItem = {
  id: string
  name: string
  description: string
  price: string
  image: string
}

interface DrawerCartProps {
  items?: CartItem[]
}

const defaultItems: CartItem[] = [
  {
    id: '1',
    name: 'Polarised sunglasses',
    description: 'Polarized sunglasses with UV protection',
    price: '$199.99',
    image: 'https://cdn.shadcnstudio.com/ss-assets/blocks/ecommerce/shopping-cart/image-7.png'
  },
  {
    id: '2',
    name: 'Lyocell-blend bucket hat',
    description: 'Bucket hat in woven fabric made from a lyocell and nylon blend.',
    price: '$19',
    image: 'https://cdn.shadcnstudio.com/ss-assets/blocks/ecommerce/shopping-cart/image-6.png'
  },
  {
    id: '3',
    name: 'Regular Fit Polo shirt',
    description: 'Regular fit polo shirt in breathable fabric.',
    price: '$29',
    image: 'https://cdn.shadcnstudio.com/ss-assets/blocks/ecommerce/shopping-cart/image-5.png'
  }
]

const DrawerCart = ({ items = defaultItems }: DrawerCartProps) => {
  return (
    <Drawer direction='right'>
      <DrawerTrigger asChild>
        <Button variant='outline'>
          <ShoppingCartIcon />{' '}
          Cart
        </Button>
      </DrawerTrigger>
      <DrawerContent>
        <DrawerHeader>
          <DrawerTitle>Cart</DrawerTitle>
        </DrawerHeader>
        <div className='no-scrollbar space-y-4 overflow-y-auto px-4'>
          {items.map((item, index) => (
            <div key={item.id}>
              {index > 0 && <Separator key={`sep-${item.id}`} className='my-4' />}
              <div key={item.id} className='space-y-4'>
                <div className='flex items-start gap-4'>
                  <div className='size-18 overflow-hidden rounded-lg border'>
                    <img src={item.image} alt={item.name} />
                  </div>
                  <div className='flex-1 space-y-2'>
                    <h4 className='font-medium'>{item.name}</h4>
                    <p className='text-muted-foreground text-sm'>{item.description}</p>
                    <p className='font-medium'>{item.price}</p>
                  </div>
                </div>
                <Button
                  variant='outline'
                  className='border-destructive text-destructive hover:bg-destructive/10 hover:text-destructive focus-visible:border-destructive focus-visible:ring-destructive/20 dark:focus-visible:ring-destructive/40 w-full'
                >
                  <Trash2Icon />
                  Remove
                </Button>
              </div>
            </div>
          ))}
          <div className='my-4 space-y-2'>
            <div className='flex justify-between'>
              <p className='text-muted-foreground'>Subtotal</p>
              <p>$247.99</p>
            </div>
            <div className='flex justify-between'>
              <p className='text-muted-foreground'>Shipping</p>
              <p>$10.00</p>
            </div>
            <Separator />
            <div className='flex justify-between'>
              <p className='font-medium'>Total</p>
              <p className='font-medium'>$257.99</p>
            </div>
          </div>
        </div>
        <DrawerFooter>
          <Button>
            Checkout{' '}
            <ArrowRightIcon />
          </Button>
          <DrawerClose asChild>
            <Button variant='outline'>Continue Shopping</Button>
          </DrawerClose>
        </DrawerFooter>
      </DrawerContent>
    </Drawer>
  )
}

export default DrawerCart
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
