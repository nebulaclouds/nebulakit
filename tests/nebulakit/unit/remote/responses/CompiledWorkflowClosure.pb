
�
�
�nebulatesterdevelopment"Acookbook.sample_workflows.formula_1.outer.StaticSubWorkflowCaller*(4a57f2327b90d0ff1a99890f38518035feb7d832 B
+
)
outer_a
Input for inner workflow

	wf_output
"

start-node"?
end-node3
	wf_output&$
identity-wf-executiontask_output"�
identity-wf-execution
identity_wf_execution" * 
a

start-nodeouter_a:��nebulatesterdevelopment":cookbook.sample_workflows.formula_1.inner.IdentityWorkflow*(4a57f2327b90d0ff1a99890f38518035feb7d832*3
	wf_output&$
identity-wf-executiontask_output�:#
identity-wf-execution

end-node:%

start-node
identity-wf-executionB#
end-node
identity-wf-executionB%
identity-wf-execution

start-node�
�
�nebulatesterdevelopment":cookbook.sample_workflows.formula_1.inner.IdentityWorkflow*(4a57f2327b90d0ff1a99890f38518035feb7d832 >
%
#
a
Input for inner workflow

task_output
"

start-node"1
end-node%
task_output

odd-nums-taskout"�

odd-nums-task

odd_nums_task" * 
num

start-nodea2~
|nebulatesterdevelopment"4cookbook.sample_workflows.formula_1.inner.inner_task*(4a57f2327b90d0ff1a99890f38518035feb7d832*%
task_output

odd-nums-taskoutx:

odd-nums-task

end-node:

start-node

odd-nums-taskB

odd-nums-task

start-nodeB
end-node

odd-nums-task�
�
|nebulatesterdevelopment"4cookbook.sample_workflows.formula_1.inner.inner_task*(4a57f2327b90d0ff1a99890f38518035feb7d832python-task0.5.0python" * "


num


out
2�
Edocker.io/lyft/nebulaexamples:4a57f2327b90d0ff1a99890f38518035feb7d832service_venvpynebula-execute
--task-module)cookbook.sample_workflows.formula_1.inner--task-name
inner_task--inputs
{{.input}}--output-prefix{{.outputPrefix}}" *7
!NEBULA_INTERNAL_CONFIGURATION_PATH/root/local.config*]
NEBULA_INTERNAL_IMAGEEdocker.io/lyft/nebulaexamples:4a57f2327b90d0ff1a99890f38518035feb7d832*%
NEBULA_INTERNAL_PROJECTnebulatester*$
NEBULA_INTERNAL_DOMAINdevelopment*
NEBULA_INTERNAL_NAME*B
NEBULA_INTERNAL_VERSION(4a57f2327b90d0ff1a99890f38518035feb7d832