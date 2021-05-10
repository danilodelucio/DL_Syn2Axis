try:
    # Figuring out the group name
    for index in nuke.selectedNodes():
        groupName = index.name()
        print(groupName)

    # Moving into the group node
    groupNode = nuke.toNode(groupName)

    with groupNode:
        # Selecting all Sphere nodes
        for index in nuke.allNodes():
            nodeClass = index.Class()
            if nodeClass.__contains__("Sphere"):
                index.setSelected(True)
                sphere_name = index.name()

        # Creating a new Scene node
        dl_scene = nuke.nodes.Scene(name="DL_Scene")

        # Getting the Translate values from Spheres nodes, and creating Axis nodes
        n = nuke.selectedNodes()
        for i in n:
            sphere_t = i['translate'].getValue()

            axis_node = nuke.createNode("Axis", inpanel=False)
            axis_node['translate'].setValue(sphere_t)
            axis_node_t = axis_node['translate'].getValue()
            for index in nuke.selectedNodes():
                axis_name = index.name()
            axis_node.setSelected(False)

        # Selecting all Axis nodes and setting the output to DL_Scene node
        axis_nodes = nuke.allNodes(filter="Axis")
        for index, axis in enumerate(axis_nodes):
            dl_scene.setInput(index, axis)

        # Selecting all Axis nodes and DL_Scene node (by index name)
        for index in nuke.allNodes():
            nodeName = index.name()
            if nodeName.__contains__("Axis"):
                index.setSelected(True)
            elif nodeName.__contains__("DL_Scene"):
                index.setSelected(True)

        # Copying all selected nodes, and deleting them
        nuke.nodeCopy("%clipboard%")
        for i in nuke.selectedNodes():
            nuke.delete(i)

    # Pasting the data from Clipboard to main Node Graph
    nuke.nodePaste("%clipboard%")

    print("[ ----- DONE! ----- ]")

except:
    print("[ ----- ERROR! ----- ]")
    print("Invalid node. Please select the group node from SynthEyes and try again!")
    print()

