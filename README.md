# MBDA TFM - Zygarde Job Executor

## Platform for the reactive training of models in the cloud

---

One of the most common applications of machine learning techniques is the creation of models intended to yield predictions on classification or regression tasks. The crafting of these models is carried out by means of algorithms that perform a training process on large volumes of data, which are representative of the domain of discourse to be inferred. In addition, every one of these techniques is likely to hold a series of configuration parameters whose values also determine the performance of the algorithm, making it necessary to find the optimal combination of them which makes for the best possible model on the dataset supplied. Due to the huge volume of data needed to build a model capable of yielding accurate predictions on a rather complex scenery, along to the trial and error process required for identifying the appropriate algorithm and the optimal hyperparameter configuration, these models' training appoints itself as a process which demands large amounts of time and computational resources.

Traditionally, the execution of highly resource-consuming processes has been carried out on supercomputers which, due to their acquisition and maintenance expenses, were only accessible to governmental, military, and academic institutions. In such a context, distributed computing techniques enable the division of computational processes into smaller units to be shared out between a set of interconnected lesser powered computers, making it feasible for affordable equipment to execute such intensive computing processes. The coming of cloud technologies, and specifically the irruption of public cloud providers, brought with it the ability to execute computational processes without any need for a prior investment in infrastructure, via an either pay-per-deployment or pay-per-use model over the hardware resources having been provisioned.

The present Master Thesis' proposal is the design and implementation of a cloud-managed and event-driven platform for training machine learning models on demand. It aims at automating the selection of the optimal learning technique and hyperparameter configuration through the parallel execution of multiple combinations of them, building the most accurate model for solving a given problem. Such a goal is fulfilled by making the most of the existence of distributed and scalable implementations of machine learning algorithms and the availability of resources from the cloud provider. Thus, the adoption of the platform being proposed provides its users with two prominent advantages: the reduction of the training global time and the intelligent management of provisioned resources, dynamically acquiring and releasing them based on the system's current workload and just paying for their actual usage period.

---

**Keywords:** machine learning, cloud architecture, distributed computing.
