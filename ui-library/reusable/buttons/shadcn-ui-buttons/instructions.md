npx shadcn@latest add @ss-components/button-06

import { Button } from '@/components/ui/button'

const ButtonActionsDemo = () => {
return (
<div className='flex flex-wrap items-center gap-4'>
<Button variant='secondary'>Cancel</Button>
<Button>Save Changes</Button>
</div>
)
}

export default ButtonActionsDemo
