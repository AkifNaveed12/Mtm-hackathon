npx shadcn@latest add @ss-components/button-16

import { Button } from '@/components/ui/button'
import { ArrowLeftIcon } from 'lucide-react'

const ButtonGhostDemo = () => {
return (
<Button variant='ghost' className='group'>
<ArrowLeftIcon className='transition-transform duration-200 group-hover:-translate-x-0.5' />
Go to settings
</Button>
)
}

export default ButtonGhostDemo
