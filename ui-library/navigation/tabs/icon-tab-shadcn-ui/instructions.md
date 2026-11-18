Create a shadcn component variant in the codebase.

The codebase should support following:

- Shadcn project structure
- React ^19
- Tailwind CSS ^4
- TypeScript ^5

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind CSS v4 or Typescript.

Shadcn Registry Dependencies:

```bash
npx shadcn@latest add tabs
```

Copy-paste this file to `components/shadcn-studio/tabs` folder:

```tsx
tabs-03.tsx
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { BookIcon, HeartIcon, GiftIcon } from 'lucide-react'

const tabs = [
  {
    name: 'Explore',
    value: 'explore',
    icon: (
      <BookIcon />
    ),
    content: (
      <>
        Discover <span className='text-foreground font-semibold'>fresh ideas</span>, trending topics, and hidden gems
        curated just for you. Start exploring and let your curiosity lead the way!
      </>
    )
  },
  {
    name: 'Favorites',
    value: 'favorites',
    icon: (
      <HeartIcon />
    ),
    content: (
      <>
        All your <span className='text-foreground font-semibold'>favorites</span> are saved here. Revisit articles,
        collections, and moments you love, any time you want a little inspiration.
      </>
    )
  },
  {
    name: 'Surprise',
    value: 'surprise',
    icon: (
      <GiftIcon />
    ),
    content: (
      <>
        <span className='text-foreground font-semibold'>Surprise!</span> Here&apos;s something unexpected - a fun fact,
        a quirky tip, or a daily challenge. Come back for a new surprise every day!
      </>
    )
  }
]

const TabsWithIconDemo = () => {
  return (
    <div className='w-full max-w-md'>
      <Tabs defaultValue='explore' className='gap-4'>
        <TabsList>
          {tabs.map(({ icon, name, value }) => (
            <TabsTrigger key={value} value={value} className='gap-1 px-2.5 sm:px-3'>
              {icon}
              {name}
            </TabsTrigger>
          ))}
        </TabsList>

        {tabs.map(tab => (
          <TabsContent key={tab.value} value={tab.value}>
            <p className='text-muted-foreground text-sm'>{tab.content}</p>
          </TabsContent>
        ))}
      </Tabs>
    </div>
  )
}

export default TabsWithIconDemo
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

npx shadcn@latest add @ss-components/tabs-03

import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { BookIcon, HeartIcon, GiftIcon } from 'lucide-react'

const tabs = [
{
name: 'Explore',
value: 'explore',
icon: (
<BookIcon />
),
content: (
<>
Discover <span className='text-foreground font-semibold'>fresh ideas</span>, trending topics, and hidden gems
curated just for you. Start exploring and let your curiosity lead the way!
</>
)
},
{
name: 'Favorites',
value: 'favorites',
icon: (
<HeartIcon />
),
content: (
<>
All your <span className='text-foreground font-semibold'>favorites</span> are saved here. Revisit articles,
collections, and moments you love, any time you want a little inspiration.
</>
)
},
{
name: 'Surprise',
value: 'surprise',
icon: (
<GiftIcon />
),
content: (
<>
<span className='text-foreground font-semibold'>Surprise!</span> Here&apos;s something unexpected - a fun fact,
a quirky tip, or a daily challenge. Come back for a new surprise every day!
</>
)
}
]

const TabsWithIconDemo = () => {
return (
<div className='w-full max-w-md'>
<Tabs defaultValue='explore' className='gap-4'>
<TabsList>
{tabs.map(({ icon, name, value }) => (
<TabsTrigger key={value} value={value} className='gap-1 px-2.5 sm:px-3'>
{icon}
{name}
</TabsTrigger>
))}
</TabsList>

        {tabs.map(tab => (
          <TabsContent key={tab.value} value={tab.value}>
            <p className='text-muted-foreground text-sm'>{tab.content}</p>
          </TabsContent>
        ))}
      </Tabs>
    </div>

)
}

export default TabsWithIconDemo
