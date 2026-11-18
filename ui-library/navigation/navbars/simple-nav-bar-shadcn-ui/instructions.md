Create a shadcn component variant in the codebase.

The codebase should support following:

- Shadcn project structure
- React ^19
- Tailwind CSS ^4
- TypeScript ^5

If it doesn't, provide instructions on how to setup project via shadcn CLI, install Tailwind CSS v4 or Typescript.

Shadcn Registry Dependencies:

```bash
npx shadcn@latest add menubar
```

Copy-paste this file to `components/shadcn-studio/menubar` folder:

```tsx
menubar-08.tsx
'use client'

import { useState } from 'react'

import {
  Menubar,
  MenubarCheckboxItem,
  MenubarContent,
  MenubarItem,
  MenubarMenu,
  MenubarRadioGroup,
  MenubarRadioItem,
  MenubarSeparator,
  MenubarShortcut,
  MenubarTrigger
} from '@/components/ui/menubar'

const MenuBarMixedDemo = () => {
  const [notifications, setNotifications] = useState({
    likes: true,
    comments: true,
    follows: false,
    mentions: true
  })

  const [feedFilter, setFeedFilter] = useState('following')

  return (
    <div className='flex flex-col items-center justify-center space-y-4'>
      <div className='text-muted-foreground text-sm font-medium'>
        Mixed Interactions Variant - Social Media Dashboard
      </div>
      <Menubar>
        <MenubarMenu>
          <MenubarTrigger>Feed</MenubarTrigger>
          <MenubarContent>
            <MenubarRadioGroup value={feedFilter} onValueChange={setFeedFilter}>
              <MenubarRadioItem value='following'>Following</MenubarRadioItem>
              <MenubarRadioItem value='trending'>Trending</MenubarRadioItem>
              <MenubarRadioItem value='latest'>Latest</MenubarRadioItem>
            </MenubarRadioGroup>
            <MenubarSeparator />
            <MenubarItem>
              Refresh Feed <MenubarShortcut>⌘R</MenubarShortcut>
            </MenubarItem>
            <MenubarItem>Mark All Read</MenubarItem>
          </MenubarContent>
        </MenubarMenu>
        <MenubarMenu>
          <MenubarTrigger>Notifications</MenubarTrigger>
          <MenubarContent>
            <MenubarCheckboxItem
              checked={notifications.likes}
              onCheckedChange={checked => setNotifications(prev => ({ ...prev, likes: checked }))}
            >
              Likes
            </MenubarCheckboxItem>
            <MenubarCheckboxItem
              checked={notifications.comments}
              onCheckedChange={checked => setNotifications(prev => ({ ...prev, comments: checked }))}
            >
              Comments
            </MenubarCheckboxItem>
            <MenubarCheckboxItem
              checked={notifications.follows}
              onCheckedChange={checked => setNotifications(prev => ({ ...prev, follows: checked }))}
            >
              New Followers
            </MenubarCheckboxItem>
            <MenubarCheckboxItem
              checked={notifications.mentions}
              onCheckedChange={checked => setNotifications(prev => ({ ...prev, mentions: checked }))}
            >
              Mentions
            </MenubarCheckboxItem>
            <MenubarSeparator />
            <MenubarItem>Notification Settings</MenubarItem>
          </MenubarContent>
        </MenubarMenu>
        <MenubarMenu>
          <MenubarTrigger>Post</MenubarTrigger>
          <MenubarContent>
            <MenubarItem>
              New Post <MenubarShortcut>⌘N</MenubarShortcut>
            </MenubarItem>
            <MenubarItem>Schedule Post</MenubarItem>
            <MenubarItem>Drafts</MenubarItem>
            <MenubarSeparator />
            <MenubarItem>Media Library</MenubarItem>
            <MenubarItem>Analytics</MenubarItem>
          </MenubarContent>
        </MenubarMenu>
        <MenubarMenu>
          <MenubarTrigger>Account</MenubarTrigger>
          <MenubarContent>
            <MenubarItem>
              Profile <MenubarShortcut>⌘P</MenubarShortcut>
            </MenubarItem>
            <MenubarItem>Settings</MenubarItem>
            <MenubarSeparator />
            <MenubarItem>Help & Support</MenubarItem>
            <MenubarItem>Sign Out</MenubarItem>
          </MenubarContent>
        </MenubarMenu>
      </Menubar>
    </div>
  )
}

export default MenuBarMixedDemo
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

npx shadcn@latest add @ss-components/menubar-08

'use client'

import { useState } from 'react'

import {
Menubar,
MenubarCheckboxItem,
MenubarContent,
MenubarItem,
MenubarMenu,
MenubarRadioGroup,
MenubarRadioItem,
MenubarSeparator,
MenubarShortcut,
MenubarTrigger
} from '@/components/ui/menubar'

const MenuBarMixedDemo = () => {
const [notifications, setNotifications] = useState({
likes: true,
comments: true,
follows: false,
mentions: true
})

const [feedFilter, setFeedFilter] = useState('following')

return (
<div className='flex flex-col items-center justify-center space-y-4'>
<div className='text-muted-foreground text-sm font-medium'>
Mixed Interactions Variant - Social Media Dashboard
</div>
<Menubar>
<MenubarMenu>
<MenubarTrigger>Feed</MenubarTrigger>
<MenubarContent>
<MenubarRadioGroup value={feedFilter} onValueChange={setFeedFilter}>
<MenubarRadioItem value='following'>Following</MenubarRadioItem>
<MenubarRadioItem value='trending'>Trending</MenubarRadioItem>
<MenubarRadioItem value='latest'>Latest</MenubarRadioItem>
</MenubarRadioGroup>
<MenubarSeparator />
<MenubarItem>
Refresh Feed <MenubarShortcut>⌘R</MenubarShortcut>
</MenubarItem>
<MenubarItem>Mark All Read</MenubarItem>
</MenubarContent>
</MenubarMenu>
<MenubarMenu>
<MenubarTrigger>Notifications</MenubarTrigger>
<MenubarContent>
<MenubarCheckboxItem
checked={notifications.likes}
onCheckedChange={checked => setNotifications(prev => ({ ...prev, likes: checked }))} >
Likes
</MenubarCheckboxItem>
<MenubarCheckboxItem
checked={notifications.comments}
onCheckedChange={checked => setNotifications(prev => ({ ...prev, comments: checked }))} >
Comments
</MenubarCheckboxItem>
<MenubarCheckboxItem
checked={notifications.follows}
onCheckedChange={checked => setNotifications(prev => ({ ...prev, follows: checked }))} >
New Followers
</MenubarCheckboxItem>
<MenubarCheckboxItem
checked={notifications.mentions}
onCheckedChange={checked => setNotifications(prev => ({ ...prev, mentions: checked }))} >
Mentions
</MenubarCheckboxItem>
<MenubarSeparator />
<MenubarItem>Notification Settings</MenubarItem>
</MenubarContent>
</MenubarMenu>
<MenubarMenu>
<MenubarTrigger>Post</MenubarTrigger>
<MenubarContent>
<MenubarItem>
New Post <MenubarShortcut>⌘N</MenubarShortcut>
</MenubarItem>
<MenubarItem>Schedule Post</MenubarItem>
<MenubarItem>Drafts</MenubarItem>
<MenubarSeparator />
<MenubarItem>Media Library</MenubarItem>
<MenubarItem>Analytics</MenubarItem>
</MenubarContent>
</MenubarMenu>
<MenubarMenu>
<MenubarTrigger>Account</MenubarTrigger>
<MenubarContent>
<MenubarItem>
Profile <MenubarShortcut>⌘P</MenubarShortcut>
</MenubarItem>
<MenubarItem>Settings</MenubarItem>
<MenubarSeparator />
<MenubarItem>Help & Support</MenubarItem>
<MenubarItem>Sign Out</MenubarItem>
</MenubarContent>
</MenubarMenu>
</Menubar>
</div>
)
}

export default MenuBarMixedDemo
